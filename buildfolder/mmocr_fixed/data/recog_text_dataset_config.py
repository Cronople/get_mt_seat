data_root = 'data/image'
train_ann_file = '../annotation/trian_file.txt'
test_ann_file = '../annotation/test_file.txt'

train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', img_scale=(280, 80)),
    dict(type='Normalize', mean=[127.5, 127.5, 127.5], std=[127.5, 127.5, 127.5]),
    dict(type='ToTensor'),
    dict(type='Collect', keys=['img', 'gt_label'])
]

test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='Resize', img_scale=(280, 80)),
    dict(type='Normalize', mean=[127.5, 127.5, 127.5], std=[127.5, 127.5, 127.5]),
    dict(type='ToTensor'),
    dict(type='Collect', keys=['img'])
]

train_data = dict(
    type='RecogTextDataset',
    data_root=data_root,
    ann_file=train_ann_file,
    pipeline=train_pipeline
)

val_data = dict(
    type='RecogTextDataset',
    data_root=data_root,
    ann_file=test_ann_file,
    pipeline=test_pipeline
)