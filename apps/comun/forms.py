from django import forms


class AbtractModelForm(forms.ModelForm):
    
    class Meta:
        exclude = ['created_by', 'deleted','updated_by', 'created_at', 'updated_at', 'deleted_at']
        abstract = True
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AbtractModelForm, self).__init__(*args, **kwargs)
        
    def save(self, commit=True):
        instance = super(AbtractModelForm, self).save(commit=False)
        if instance.id is None:        
            instance.created_by = self.user
        else:
            instance.updated_by = self.user
            
        if commit:
            instance.save()
        return instance
        