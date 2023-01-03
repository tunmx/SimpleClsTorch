config_default = """save_dir: workspace/resnet50
model:
  name: ResNetVertex
  option:
    depth: 50
  loss:
    name: mse_loss
  weight: null
data:
  train:
    name: LabelMeDataset
    option:
      img_path: oinbagCrawler_vertex_train/train
      labels_path: null
      mode: train
    batch_size: 128
  val:
    name: LabelMeDataset
    option:
      img_path: oinbagCrawler_vertex_train/val
      labels_path: null
      mode: val
    batch_size: 128
  pipeline:
    image_size: [112, 112]
    sometimes_rate: 0.5
    crop_percent: [0, 0.1]
    flip_lr: 0.5
    gaussian_blur: [0, 1.0]
    multiply: [0.25, 1.55]
    contrast_normalization: [0.8, 1.2]
    gamma_contrast: [0.9, 1.2]
    scale_x: [0.8, 1.6]
    scale_y: [0.8, 1.6]
    translate_percent_x: [-0.15, 0.15]
    translate_percent_y: [-0.15, 0.15]
    rotate: [-25, 25]
    shear: [-25, 25]
    order: [0, 1]
    cval: 0
    mode: constant
trainer:
  worker_num: 0
  epoch_num: 150
  optimizer:
    name: Adam
    lr: 0.001
  schedule:
    name: 'ReduceLROnPlateau'
    mode: 'min'
    factor: 0.5
    patience: 5
    verbose: True
wandb:
  team_name: tunm
  project_name: LP-Vertex
  experiment_name: exp
  scenario_name: training
  folder: log
  key: 4b49a6b0286dcfb718a12360108a7a8578c3582c
"""
