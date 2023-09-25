# Train Offline, Test Online: A Real Robot Learning Benchmark
<!-- TODO(Kathy): add teaser figures, some setup/task images, etc  -->
## Phase 1: Simulation
1. [Software installation](#software-installation)
2. [Simulator installation](#simulator-installation)
3. [Download our simulation dataset](#download-our-simulation-dataset)
4. [(Optional) Train a TOTO Behavior Cloning Agent](#train-a-toto-behavior-cloning-agent)
5. [Evaluating your agent](#simulation-evaluation)

## Phase 2: Real World
1. [Software installation](#software-installation)
3. [Download our real-world dataset](#download-our-real-world-dataset)
4. [(Optional) Train a TOTO Behavior Cloning Agent](#train-a-toto-behavior-cloning-agent)
5. [Submitting your agent for real-world evaluation](#real-world-evaluation)

## Submitting your custom agent or vision representation
We invite the community to submit their custom methods to the TOTO competition. We support the following challenges:

- [**Challenge 1**](#submitting-a-custom-vision-representation): a pre-trained visual representation model. 
- [**Challenge 2**](#submitting-a-custom-policy): an agent policy which uses either a custom visual representation or the ones we provide.

![toto_dataset](docs/images/toto_dataset.gif)

## Prerequisites
- Conda

## Installation
You can either use a local conda environment or a docker environment.

### Setup conda environment
1. Run the following command to create a new conda environment: ```source setup_toto_env.sh```

### Setup docker environment
1. Follow the instructions in [here](https://github.com/AGI-Labs/toto_benchmark/blob/main/docker/README.md).

Note: If you are contributing models to TOTO, we strongly suggest setting up the docker environment.

### (Optional) Download our vision representation models
We release our vision representation models [here](https://drive.google.com/drive/folders/1iqDIIIalTi3PhAnFjZxesksvFVldK42p?usp=sharing).This contains the in-domain models (MoCo and BYOL) that are trained with the TOTO dataset.

## Simulator installation
Our pouring simulator uses DeepMind MuJoCo, which you can install with this command:
  ```
  pip install mujoco
  ```
To set up MuJoCo rendering, install egl following the instructions [here](https://pytorch.org/rl/reference/generated/knowledge_base/MUJOCO_INSTALLATION.html#prerequisite-for-rendering-all-mujoco-versions).

You can check that the environment is properly installed by running the following from the toto_benchmark directory:
  ```
  (toto-benchmark) user@machine:~$ MUJOCO_GL=egl python
  Python 3.8.0 | packaged by conda-forge | (default, Nov 22 2019, 19:11:38)
  [GCC 7.3.0] :: Anaconda, Inc. on linux
  Type "help", "copyright", "credits" or "license" for more information.
  >>> from toto_benchmark.sim.dm_pour import DMWaterPouringEnv
  >>> eval_env = DMWaterPouringEnv()
  ```

## Download our simulation dataset
The simulation dataset can be downloaded [here](https://drive.google.com/drive/folders/1HKtjLBgI6FJlMj44Tbr_cDPUCCz-mEZO?usp=sharing). The file contains 103 human teleoperated trajectories of our pouring task.

## Simulation evaluation
To evaluate an agent following the BC training provided in the example train.py script, run the following command:
  ```
python toto_benchmark/scripts/eval_agent.py -f outputs/<path_to>/<agent>/
  ```
If you wish to evaluate a custom agent, replace the agent_predict_fn indicated by the TODO(optional) in toto_benchmark/scripts/eval_agent.py.

## Download our real-world dataset
TOTO consists of two tabletop manipulation tasks, scooping and pouring. The datasets of the two tasks can be downloaded [here](https://drive.google.com/drive/folders/1JGPGjCqUP4nUOAxY3Fpx3PjUQ_loo7fc?usp=sharing).

*Update*: please download the scooping data from Google Cloud Bucket [here](https://console.cloud.google.com/storage/browser/toto-dataset) instead.

<!-- TODO: update link to dataset README.md file. May consider create a dataset/ folder and add the readme into the repo -->
We release the following datasets: 
- `cloud-dataset-scooping.zip`: TOTO scooping dataset
- `cloud-dataset-pouring.zip`: TOTO pouring dataset

Additional Info:
- `scooping_parsed_with_embeddings_moco_conv5.pkl`: the same scooping dataset parsed with MOCO (Ours) pre-trained visual representations. (included as part of the TOTO scooping dataset) 
- `pouring_parsed_with_embeddings_moco_conv5.pkl`: the same pouring dataset parsed with MOCO (Ours) pre-trained visual representations. 
(included as part of the TOTO pouring dataset)

For more detailed dataset format information, see `assets/README.md`

## Simulation submission
- Submit your zipped folder for evaluation using this [google form](https://docs.google.com/forms/d/e/1FAIpQLSdOCCoRnXj7W_laT9wyqqW-ks4mkmJjYLydmfMmILMub7l0VQ/viewform).

## Real-world evaluation
<!-- TODO(Kathy): port over instructions from website? -->

## Train a TOTO Behavior Cloning Agent
Here's an example command to train an image-based behavior cloning (BC) agent on the real-world data with MOCO (Ours) as the image encoder. Our BC agent assumes that each image has been encoded into a 1D vector. You will need to download `scooping_parsed_with_embeddings_moco_conv5_robocloud.pkl` to have this launched.

```
cd toto_benchmark
 
python scripts/train.py --config-name train_bc.yaml data.pickle_fn=../assets/cloud-dataset-scooping/scooping_parsed_with_embeddings_moco_conv5_robocloud.pkl
```

The config train_bc_sim.yaml is set up to train a BC agent on the simulated pouring task (phase 1). Before launching the command, [download our simulation dataset](#download-our-simulation-dataset) and put the file under `toto_benchmark/sim`:
  ```
python scripts/train.py --config-name train_bc_sim.yaml
  ```

<!-- TODO: instructions on training agents with other vision representations? need to parse the dataset, etc -->


## Submitting a custom vision representation

To submit your custom visual representation model to TOTO, you will train your visual representation model in any preferred way, generate image embeddings for TOTO datasets with your model, and finally train and submit a BC agent on this dataset. You will submit both your visual representation model and the BC model, as your visual representation model will be loaded and called during evaluations. We have provided scripts for interfacing with your vision model and for BC training. Please see the following instructions for details. 

*Note that you may or may not use TOTO datasets when training your visual representation model.*

<!-- TODO: mention somewhere the assumption that our BC pipeline assume your image embedding to be a 1D vector? -->
- Download the datasets [here](https://drive.google.com/drive/folders/1JGPGjCqUP4nUOAxY3Fpx3PjUQ_loo7fc?usp=share_link).
- Move and unzip the datasets in `assets/`, so it has the following structure:
    ```
    assets/
    - cloud-dataset-scooping/
        - data/
    - cloud-dataset-pouring/
        - data/
    ```
- Train the model in your preferred way. If you plan to train it on our datasets, feel free to use the provided `assets/example_load.py` for loading images in our datasets.
<!-- TODO: add example_load.py to github, and update this with a link -->

- After your model is trained, update the file `toto_benchmark/vision/CollaboratorEncoder.py` for loading your model, as well as any transforms needed. Feel free to include additional files needed by your model under `toto_benchmark/vision/`.
    - The functions defined in `CollaboratorEncoder.py` take in a config file. An example config file `toto_benchmark/conf/train_bc.yaml` has been provided. You may specify `vision_model_path` in the config file for loading your model, as well as add additional keys if needed. You will use this config when training a BC agent later.
    - Please make sure your vision model files are outside of `assets/`, as it will be ignored when generating files for submission later.

- Update your model's embedding size in `toto_benchmark/vision/__init__.py`.
- Launch `data_with_embeddings.py` to generate a dataset with image embeddings generated by your model. 

    ```
    # Example command for the scooping dataset: 
    cd toto_benchmark

    python scripts/data_with_embeddings.py --data_folder ../assets/cloud-dataset-scooping/ --vision_model collaborator_encoder 
    ```
    After this, a new data file `assets/cloud-dataset-scooping/parsed_with_embeddings_collaborator_encoder.pkl` will be generated. 
- Now we are ready to train a BC agent! Here's an example command for training with config `train_bc.yaml`:
    ```
    python scripts/train.py --config-name train_bc.yaml data.pickle_fn=../assets/cloud-dataset-scooping/parsed_with_embeddings_collaborator_encoder.pkl agent.vision_model='collaborator_encoder'
    ```
    A new agent folder will be created in `outputs/<path_to>/<agent>/`.
- Once the above is done, run `python scripts/test_stub_env.py -f outputs/<path_to>/<agent>/` for a simple simulated test on the robot. If everything works as expected, we are ready to have the agent to be evaluated on the real robot!
- For submission, Run ```prepare_submission.sh``` script to generate a zipped folder which is ready for submission.
- Submit your zipped folder for evaluation using this [google form](https://forms.gle/hJWPaXK1DcpuJnhQA).
- We will evaluate your agents on the robot hardware and update your position on the leaderboard.

## Submitting a custom policy
To submit your agent, you will train your image-based agent on our datasets in any preferred way. You may develop your custom visual representation model or use existing ones in TOTO. Please see below for detailed instructions: 
- Download the datasets [here](https://drive.google.com/drive/folders/1JGPGjCqUP4nUOAxY3Fpx3PjUQ_loo7fc?usp=share_link) and train your agents in your preferred way.
- *(Optional)* If you plan to use any existing TOTO visual representation model, we release the pre-trained models [here](https://drive.google.com/drive/folders/1iqDIIIalTi3PhAnFjZxesksvFVldK42p?usp=sharing). Download the models and put them into `assets/`. Then, simply use our provided functions to load the models as follows:
    ```
    from toto_benchmark.vision import load_model, load_transforms
    img_encoder = load_model(config)
    transforms = load_transforms(config)
    
    # See conf/train_bc.yaml for an example config file.
    ``` 
- Update the agent file: `toto_benchmark/agents/CollaboratorAgent.py`. This acts as a wrapper around your model to interface with our robot stack. Please refer to `toto_benchmark/agents/Agent.py` for more information
- Update the agent config file `toto_benchmark/outputs/collaborator_agent/hydra.yaml` for initializing your agent
- Once the above is done, run 
    ```
    cd toto_benchmark

    python scripts/test_stub_env.py -f outputs/collaborator_agent/
    ``` 
for a simple simulated test on the robot. If everything works as expected, we are ready to have the agent to be evaluated on the real robot!
- For submission, Run ```prepare_submission.sh``` script to generate a zipped folder which is ready for submission.
    - Please make sure your agent files are outside of `assets/`, as it will be ignored for submission.
- Submit your zipped folder for evaluation using this [google form](https://forms.gle/hJWPaXK1DcpuJnhQA).
- We will evaluate your agents on the robot hardware and update your position on the leaderboard.

## Citation

If you use TOTO, consider citing the original paper:

```
@inproceedings{zhou2023train,
  author={Zhou, Gaoyue and Dean, Victoria and Srirama, Mohan Kumar and Rajeswaran, Aravind and Pari, Jyothish and Hatch, Kyle and Jain, Aryan and Yu, Tianhe and Abbeel, Pieter and Pinto, Lerrel and Finn, Chelsea and Gupta, Abhinav},
  booktitle={2023 IEEE International Conference on Robotics and Automation (ICRA)}, 
  title={Train Offline, Test Online: A Real Robot Learning Benchmark}, 
  year={2023},
 }
```
