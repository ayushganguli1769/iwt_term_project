from django.db import models
class Question(models.Model):
    display_text = models.CharField(max_length=400,blank= False, null= True)
    filled = models.BooleanField(default= False)
    answer = models.CharField(max_length=400,blank= False, null= True)
    def __str__(self):
        return self.display_text
    
class subQuestion(models.Model):
    main_question = models.ForeignKey(Question,on_delete = models.CASCADE)
    sub_question_display_text = models.CharField(max_length=400,blank= False, null= True)
    def __str__(self):
        return self.sub_question_display_text
    

# Create your models here.
