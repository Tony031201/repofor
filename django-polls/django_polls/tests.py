from django.test import TestCase
import datetime
from django.utils import timezone
from django.test import Client
from django.test.utils import setup_test_environment
from django.urls import reverse

from .models import Question

class QuestionModelTests(TestCase):
    def test_was_published_rencently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(),False)

    def test_was_published_rencently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_rencently_with_recent_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question=Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text,days):
    time = timezone.now() + timezone.timedelta(days=days)
    return Question.objects.create(question_text=question_text,pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        If no question exist, an appropriate message is displayed
        """
        client = Client()
        response = client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"],[])

    def test_past_question(self):
        """
        If create a past question, it should be displayed on the
        index page
        """
        client = Client()
        question = create_question(question_text="Past_question",days=-30)
        response = client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

    def test_future_question(self):
        """
        If create a future question, it should not be displayed on the
        index page
        """
        client = Client()
        question = create_question(question_text="Future_question", days=5)
        response = client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        client = Client()
        question = create_question(question_text="Past_question",days=-30)
        create_question(question_text="Future_question", days=5)
        response = client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        client = Client()
        question1 = create_question(question_text="Past_question_1", days=-30)
        question2 = create_question(question_text="Past_question_2", days=-25)
        response = client.get(reverse("polls:index"))
        self.assertQuerySetEqual(response.context["latest_question_list"],[question2,question1],)

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        future_question = create_question(question_text="Future question",days=20)
        response = self.client.get(reverse("polls:detail", args=(future_question.pk,)))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text="Past question", days=-20)
        response = self.client.get(reverse("polls:detail", args=(past_question.pk,)))
        self.assertContains(response, past_question.question_text)



# Create your tests here.
