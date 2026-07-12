from typing import Union, Optional, List

import numpy as np
from transformers import Pipeline, PreTrainedTokenizer


class MultiLabelPipeline(Pipeline):
    def __init__(
            self,
            model,
            tokenizer: PreTrainedTokenizer,
            threshold: float = 0.3,
            **kwargs
    ):
        super().__init__(model=model, tokenizer=tokenizer, **kwargs)
        self.threshold = threshold

    def _sanitize_parameters(self, **kwargs):
        return {}, {}, {}

    def preprocess(self, inputs):
        return self.tokenizer(
            inputs,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )

    def _forward(self, model_inputs):
        outputs = self.model(**model_inputs)
        # outputs[0] = logits (loss is outputs[0] only when labels provided)
        logits = outputs[0] if not hasattr(outputs, "logits") else outputs.logits
        return {"logits": logits}

    def postprocess(self, model_outputs):
        logits = model_outputs["logits"].detach().numpy()
        scores = 1 / (1 + np.exp(-logits))  # Sigmoid
        results = []
        for item in scores:
            labels = []
            item_scores = []
            for idx, s in enumerate(item):
                if s > self.threshold:
                    labels.append(self.model.config.id2label[idx])
                    item_scores.append(float(s))
            results.append({"labels": labels, "scores": item_scores})
        return results

    def __call__(self, inputs: Union[str, List[str]], **kwargs):
        # Handle batch input manually
        if isinstance(inputs, str):
            inputs = [inputs]

        all_results = []
        for text in inputs:
            model_inputs = self.preprocess(text)
            model_outputs = self._forward(model_inputs)
            result = self.postprocess(model_outputs)
            all_results.extend(result)
        return all_results