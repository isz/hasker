from django import forms


class BootstrapMixin:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if getattr(field.widget, "input_type", "") == "file_input":
                field.widget.attrs.update({"class": "form-control-file"})
            else:
                field.widget.attrs.update({"class": "form-control"})
