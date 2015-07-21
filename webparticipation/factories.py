# import factory
# from django.contrib.auth.hashers import make_password
# from .models import Interest, User
#
#  class UserFactory(factory.django.DjangoModelFactory):
#       """
#      Creates a standard active user.
#      """
#      class Meta:
#          model = User
#
#      first_name = 'Standard'
#      last_name = 'User'
#      # Emails must be unique - so use a sequence here:
#      email = factory.Sequence(lambda n: 'user.{}@test.test'.format(n))
#      password = make_password('pass')
#      is_active = True
#
#      @factory.post_generation
#      def interests(self, create, extracted, **kwargs):
#          """
#          Where 'interests' are defined, add them to this user.
#         """
#          if not create:
#            return
#
#         if extracted:
#             for interest in extracted:
#                 self.interest.add(interest)
#
#  class InterestFactory(factory.django.DjangoModelFactory):
#      class Meta:
#         model = Interest
#
#     name = factory.Sequence(lambda n: 'interest{}'.format(n))