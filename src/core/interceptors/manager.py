# src/core/interceptors/manager.py
from .input_interceptor import InputInterceptor
from .output_interceptor import OutputInterceptor

class InterceptorManager:
    def __init__(self):
        self.input_interceptors: list[InputInterceptor] = []
        self.output_interceptors: list[OutputInterceptor] = []
        self._load_default_interceptors()

    def _load_default_interceptors(self):
        from .implementations.file_reader import FileReaderInterceptor
        self.input_interceptors.append(FileReaderInterceptor())

    def run_input_interceptors(self, text: str) -> str:
        for interceptor in self.input_interceptors:
            if interceptor.applies(text):
                text = interceptor.process(text)
        return text

    def run_output_interceptors(self, text: str) -> str:
        for interceptor in self.output_interceptors:
            if interceptor.applies(text):
                text = interceptor.process(text)
        return text
