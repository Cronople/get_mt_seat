_base_ = [
    # '../_base_/datasets/toy_data.py',
    '../_base_/default_runtime.py',
    '../_base_/schedules/schedule_adam_step_5e.py',
    '_base_sar_resnet31_parallel-decoder.py',
]

train_cfg = dict(type='EpochBasedTrainLoop', max_epochs=100, val_interval=10)

optim_wrapper = dict(
    optimizer=dict(type='Adam', lr=5e-4, weight_decay=1e-4)
)

load_from='./save/rec_word03/epoch_90.pth'
visualizer=dict(type='Visualizer', vis_backends=[dict(type='WandbVisBackend')])

param_scheduler = [
    dict(
        type='LinearLR',
        start_factor=0.1,
        by_epoch=True,
        begin=0,
        end=5
    ),
    dict(
        type='CosineAnnealingLR',
        T_max=100,
        eta_min=1e-5,
        by_epoch=True
    )
]

default_hooks = dict(
    checkpoint=dict(
        type='CheckpointHook',
        by_epoch=False,
        interval=10,  # 20 epoch마다 저장
    ),
    early_stopping=dict(
        type='EarlyStoppingHook',
        monitor='Toy/recog/char_precision',
        patience=10,
        min_delta=0.001,
        rule='greater'
    ),
    logger=dict(
        type='LoggerHook', 
        interval=10
    )
)

# dataset settings
train_list = [
    dict(
        type='OCRDataset',
        ann_file='./data/annotation/train.json',  # JSON 라벨 파일 경로
        pipeline=None)
]
val_list = [
    dict(
        type='OCRDataset',
        ann_file='./data/annotation/val.json',
        pipeline=None)
]
default_hooks = dict(logger=dict(type='LoggerHook', interval=1))

train_dataloader = dict(
    batch_size=50,
    sampler=dict(type='DefaultSampler', shuffle=True),
    dataset=dict(
        type='ConcatDataset',
        datasets=train_list,
        pipeline=_base_.train_pipeline))

val_dataloader = dict(
    batch_size=20,
    num_workers=4,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dict(
        type='ConcatDataset',
        datasets=val_list,
        pipeline=_base_.test_pipeline))
test_dataloader = val_dataloader


val_evaluator = dict(dataset_prefixes=['Toy'])
test_evaluator = val_evaluator