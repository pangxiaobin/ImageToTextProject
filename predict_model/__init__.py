"""
定义模型预测字典，用于根据模型名称获取对应的模型预测类
"""

from .bicl_model import BICLModelPredict


MODEL_PREDICT_DICT = {"BICLModelPredict": BICLModelPredict}

__all__ = ["MODEL_PREDICT_DICT"]
