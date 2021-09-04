from students.models import Student




class StudentGraphQLView(UserPassesTestMixin, LoginRequiredMixin, GraphQLView):
    raise_exception = True

    def test_func(self):
        try:
            self.request.user.student
            return True
        except (AttributeError, Student.DoesNotExist):
            return False
