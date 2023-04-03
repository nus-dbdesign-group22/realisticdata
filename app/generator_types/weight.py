import numpy as np
from generator_types.base import BaseTypeGenerator


class Weight(BaseTypeGenerator):

    def get_next_value(self, related_values=None) -> any:
        mean_height = 170
        mean_weight = 70
        var_h = 15
        var_w = 15
        cov_h_w = 20
        if related_values:
            height = related_values[0]
            cov = np.array([[var_h, cov_h_w], [cov_h_w, var_w]])
            sample_height, sample_weight = np.random.multivariate_normal([mean_height, mean_weight], cov)
            sample = sample_weight * (height / sample_height)
        else:
            sample = np.random.normal(mean_weight, var_w)
        return round(sample, 1)
