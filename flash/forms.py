from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Flashcard, QuestionAnswer,ResearchTopic ,Chapter

class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['title']

class ChapterForm(forms.ModelForm):

    class Meta:
        model = Chapter
        fields = '__all__'


class QuestionAnswerForm(forms.ModelForm):
    class Meta:
        model = QuestionAnswer
        fields = ['chapter','question', 'answer','option']
        widgets = {
            'question': CKEditorUploadingWidget(),
            'answer': CKEditorUploadingWidget(),

           
        }
 
class ResearchTopicForm(forms.ModelForm):

    class Meta:
        model = ResearchTopic
        fields = ['description']
        widgets = {
            'description' : CKEditorUploadingWidget()
        }
        