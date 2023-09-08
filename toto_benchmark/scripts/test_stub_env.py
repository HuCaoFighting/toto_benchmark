import argparse
import numpy as np
import os
from PIL import Image
import time
import torch
import yaml

from toto_benchmark.agents import init_agent_from_config
from toto_benchmark.vision import load_model, load_transforms
from toto_benchmark.scripts.utils import Namespace

SUCCESS_MESSAGE = "Agent outputs valid action - Test passed!"
FAILURE_MESSAGE = "Agent outputs invalid action - Test failed."

'''
## Test the agent locally in a dummy environment (from docker container interactive shell)
- AGENT_PATH: should contain a hydra.yaml file either generated by the training script or manually added. Please refer to conf/train_bcimage.yaml for reference.
```
python test_stub_env.py -f ./outputs -a AGENT_PATH
```
example usage
```
cd toto_benchmark/scripts
python test_stub_env.py -f ./outputs/dummy_agent
```
'''

class DummyFrankaEnv():
    CMD_SHAPE = 7
    START_POSITION = np.array([0.1828, -0.4909, -0.0093, -2.4412, 0.2554, 0.3310, 0.0])
    
    def __init__(self, img_transform_fn):
        self.img_transform_fn = img_transform_fn

    def step(self, action=[]):
        """Creates a dummy observation
        """
        obs = {
            "inputs": self.START_POSITION
        }

        rgb_img = Image.fromarray(np.ones((480, 640, 3), dtype=np.uint8)) ## simulate the camera input
        depth_img = np.ones((480, 640))
        obs['cam0c'] = self.img_transform_fn(rgb_img)
        obs['cam0d'] = depth_img
        return obs

    def validate_action(self, action):
        return action.shape == self.START_POSITION.shape

def process_image_helper(state, imitation_state): # for bcimage_pre
    imgs = [imitation_state[_c] for _c in state['cam_in_state']]
    imgs_out = [state['img_encoder'](torch.unsqueeze(img, dim=0)).detach().numpy().reshape([1, -1]) for img in imgs]
    concat_inputs = np.hstack([imitation_state['inputs'].reshape([1, -1]), imgs_out[0]]) ### assume 1 image only
    imitation_state['inputs'] = concat_inputs.reshape([-1])
    return imitation_state

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--agent_path",
                        type=str,
                        default="./outputs")
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    with open(os.path.join(args.agent_path, 'hydra.yaml'), 'r') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)
        # Overwriting to use local
        cfg['saved_folder'] = args.agent_path
        cfg = Namespace(cfg)

    agent, img_transform_fn = init_agent_from_config(cfg, 'cuda:0')
    state = {}
    if cfg.agent.type == 'bcimage_pre':
        img_transform_fn = load_transforms(cfg)
        state['img_transform_fn'] = img_transform_fn
        state['cam_in_state'] = ['cam0c']
        state['img_encoder'] = load_model(cfg)

    env = DummyFrankaEnv(img_transform_fn)
    STEPS_PER_TIME_LOG = 100
    steps = 0
    time_taken = 0
    
    while(True):
        obs = env.step()
        start = time.time()
        if cfg.agent.type == 'bcimage_pre':
            obs = process_image_helper(state, obs)
        action = agent.predict(obs)
        end = time.time()
        time_taken += end-start

        if (steps%STEPS_PER_TIME_LOG) == 0:
            time_per_step = time_taken/STEPS_PER_TIME_LOG if steps > 0 else time_taken
            time_taken = 0
            message = SUCCESS_MESSAGE if env.validate_action(action) else FAILURE_MESSAGE
            print(f"Average time taken per agent prediction: {time_per_step}")
            print(message)
        
        steps += 1
