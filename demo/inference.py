"""
[-Benchmark-]
Model           Input       Loss        use-time@corei7         ONNX-size
--
ResNet50        112x112     2.6e-4      23ms                    96.2M
MNetV2:0.5      112x112     3.6e-4      5ms                     96.2M
MNetV2:0.35     96x96       6.5e-4      1.7ms                    2.2M
MNetV2:0.25     96x96       6.4e-4      1.3ms                    1.6M
"""

import cv2
import numpy as np
import simplecls as bvt
import click
import os
from tqdm import tqdm
import time


def backend_matching(backend):
    table = dict(torch=bvt.BACKEND_TORCH, onnx=bvt.BACKEND_ONNXRUNTIME, mnn=bvt.BACKEND_MNN)

    return table[backend]


@click.command(help='Exec inference flow.')
@click.argument('backend', type=click.Choice(['torch', 'onnx', 'mnn']))
@click.option('-config', '--config', type=click.Path(), default=None, )
@click.option('-model_path', '--model_path', type=click.Path(), default=None, )
@click.option('-data', '--data', type=click.Path(), )
@click.option('-save_dir', '--save_dir', default=None, type=click.Path(), )
@click.option('-input_shape', '--input_shape', default=None, multiple=True, nargs=2, type=int)
@click.option("-show", "--show", is_flag=True, type=click.BOOL, )
def inference(backend, config, model_path, data, save_dir, input_shape, show):
    net = None
    backend_tag = backend_matching(backend)
    if input_shape is not None:
        input_size = input_shape[0]
    else:
        input_size = (112, 112)
    data_list = list()
    if os.path.isdir(data):
        data_list = [os.path.join(data, item) for item in os.listdir(data) if
                     item.split('.')[-1].lower() in ['jpg', 'png', 'jpeg']]
    else:
        data_list.append(data)
    if backend_tag == bvt.BACKEND_TORCH:
        assert config is not None, 'use torch need input config.'
        cfg = bvt.load_cfg(config)
        model_cfg = cfg.model
        if model_path is None:
            model_path = os.path.join(cfg.save_dir, 'best_model.pth')
            assert os.path.exists(model_path), 'The model was not matched.'
        if input_shape is None:
            input_size = tuple(cfg.data.pipeline.image_size)
        infer = bvt.multiple_backend(bvt.BACKEND_TORCH)
        net = infer(weights_path=model_path, input_shape=input_size, model_name=model_cfg.name,
                    model_option=model_cfg.option)
        print(net)

    elif backend_tag == bvt.BACKEND_ONNXRUNTIME:
        assert model_path, 'Place input onnx model path.'
        infer = bvt.multiple_backend(bvt.BACKEND_ONNXRUNTIME)
        net = infer(onnx_path=model_path, input_shape=input_size)
    else:
        return NotImplementedError('not implement backend.')

    assert net is not None, 'error'

    if save_dir:
        os.makedirs(save_dir, exist_ok=True)

    sum_t = 0.0
    for path in tqdm(data_list):
        image = cv2.imread(path)
        image = cv2.resize(image, input_size)
        t = time.time()
        kps = net(image)
        ut = time.time() - t
        sum_t += ut
        h, w, _ = image.shape
        kps[:, 0] = kps[:, 0] / input_size[1] * h
        kps[:, 1] = kps[:, 1] / input_size[0] * w
        for x, y in kps.astype(np.int32):
            cv2.line(image, (x, y), (x, y), (80, 240, 100), 3)
        cv2.polylines(image, [kps.astype(np.int32)], True, (0, 0, 200), 1, )
        if show:
            cv2.imshow('image', image)
            cv2.waitKey(0)
        if save_dir:
            cv2.imwrite(os.path.join(save_dir, os.path.basename(path)), image)

    print(f"avg use time: {sum_t / len(data_list)}")


if __name__ == '__main__':
    inference()
