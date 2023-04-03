import numpy as np
from generator_types.base import BaseTypeGenerator


class Height(BaseTypeGenerator):

    def get_next_value(self, related_values=None) -> any:
        mean_height = 170
        mean_weight = 70
        var_h = 10
        var_w = 10
        cov_h_w = 10
        if related_values:
            weight = related_values[0]
            cov = np.array([[var_h, cov_h_w], [cov_h_w, var_w]])
            sample_height, sample_weight = np.random.multivariate_normal([mean_height, mean_weight], cov)
            sample = sample_height * (weight / sample_weight)
        else:
            sample = np.random.normal(mean_height, var_h)
        return round(sample)
