from deform.renderer import configure_zpt_renderer
from deform.widget import TextInputWidget, CheckboxWidget

# let deform know about our custom templates
configure_zpt_renderer(["tikzhelper:templates/deform"])

def PlaceholderTextInputWidget(placeholder, type='text'):
    w = TextInputWidget(template='placeholderinput',
                        type=type,
                        placeholder=placeholder)
    return w

def FancyCheckboxInput(label):
    w = CheckboxWidget(template='fancycheckbox',
                       css_class='custom-control-input',
                       label=label)
    return w