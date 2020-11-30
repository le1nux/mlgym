from typing import Callable, Dict, Any
import torch
from functools import partial
from sklearn.metrics import roc_auc_score, average_precision_score
from ml_gym.batch import InferenceResultBatch


def binary_auroc_score(y_true: torch.Tensor, y_pred: torch.Tensor, **params: Dict[str, Any]) -> float:
    score = roc_auc_score(y_true=y_true, y_score=y_pred, **params)
    return score


def binary_aupr_score(y_true: torch.Tensor, y_pred: torch.Tensor, **params: Dict[str, Any]) -> float:
    score = average_precision_score(y_true=y_true, y_score=y_pred, **params)
    return score


class Metric:

    def __init__(self, tag: str, identifier: str, target_subscription_key: str,
                 prediction_subscription_key: str, metric_fun: Callable, params: Dict[str, Any]):
        self.tag = tag
        self.identifier = identifier
        self.metric_fun = metric_fun
        self.params = params
        self.target_subscription_key = target_subscription_key
        self.prediction_subscription_key = prediction_subscription_key

    def __call__(self, result_batch: InferenceResultBatch) -> float:
        y_true = result_batch.get_targets(self.target_subscription_key).cpu()
        y_pred = result_batch.get_predictions(self.prediction_subscription_key).cpu()
        return self.metric_fun(y_true=y_true, y_pred=y_pred, **self.params)


class MetricFactory:
    @classmethod
    def get_partial_metric(cls, metric_key: str, metric_fun: Callable,  params: Dict = None):
        if params is None:
            params = {}

        return partial(Metric, identifier=metric_key, metric_fun=metric_fun, **params)