from rest_framework import serializers
from users.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.hashers import make_password
from users.models import EmailVerificationCode

User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username','email','phone_number','first_name','last_name')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']

    def update(self,instance,validated_data):
        password=validated_data.get('password', None)
        if password:
            validated_data['password']=make_password(password)
        return super().update(instance,validated_data)

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(required=True,write_only=True,validators=[validate_password])
    password2=serializers.CharField(required=True,write_only=True)

    class Meta:
        model=User
        fields= ['id','username','email','first_name','last_name','password','password2']

    def validate(self, attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({"password":"password dont match"})
        return attrs
        
    def create(self,validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_active=False
        user.save()
        return user

class PasswordResetSerializer(serializers.Serializer):
    email=serializers.EmailField()
    def validate_email(self,value):
        try:
            user=User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('momxmarebeli msgavsis emailit ver moidzebna')
        return value
    
class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64=serializers.CharField()
    token=serializers.CharField()
    password=serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2=serializers.CharField(write_only=True,required=True)

    def validate(self,attrs):
        if attrs['password']!=attrs['password2']:
            raise serializers.ValidationError({'password':'parolebi ar emtxveva'})
        
        try:
            uid=force_str(urlsafe_base64_decode(attrs['uidb64']))
            user=User.objects.get(pk=uid)
        except (User.DoesNotExist,ValueError,TypeError,KeyError):
            raise serializers.ValidationError({'message':'momxmarebeli ver moidzebna'})
        
        token=attrs['token']
        if not default_token_generator.check_token(user,token):
            raise serializers.ValidationError({'message':'araswori an vadagasuli tokenia'})
        
        attrs['user']=user
        return attrs
    
    def save(self):
        user=self.validated_data['user']
        user.set_password(self.validated_data['password'])
        user.save

class EmailCodeResendSerializer(serializers.Serializer):
    email=serializers.EmailField()
    
    def validate(self,attrs):
        email=attrs['email']
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message":"momxmarebeli msgavsi emailit ver moidzebna"})
        
        if user.is_active():
            raise serializers.ValidationError({"message":'momxmarebeli ukve gaaktiurebulia'})
        
        attrs['user']=user
        return attrs
    
class EmailConfirmSerializer(serializers.Serializer):
    email=serializers.EmailField()
    code=serializers.CharField()
    
    def validate(self,attrs):
        email=attrs['email']
        code=attrs['code']
        
        try:
            user=User.objects.get(email=email)
            verification_code=EmailVerificationCode.objects.get(user=user)
            
            if verification_code.code!=code:
                raise serializers.ValidationError({'message':'kodi arasworia'})
            
            if verification_code.is_expired():
                raise serializers.ValidationError({'message':'kodi vadagasulia'})
        except (User.DoesNotExist,EmailVerificationCode.DoesNotExist):
            raise serializers.ValidationError({'message':'ver moidzebna momxmarebeli an mastan dakavshirebuli kodi'})
        
        attrs['user']=user
        return attrs