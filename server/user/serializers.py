from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
import requests,os

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "password", "password2","walletAddress")
        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }

    def save(self):
        user = get_user_model()(
            email=self.validated_data["email"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
            walletAddress=self.validated_data["walletAddress"],
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]

        if len(self.validated_data["walletAddress"]) != 42:
            raise serializers.ValidationError(
                {"walletAddress": "Wallet address must be 42 characters long!"})

        if password != password2:
            raise serializers.ValidationError(
                {"password": "Passwords do not match!"})

        user.set_password(password)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "first_name", "last_name","walletAddress")

def get_balance(wallet_address):
    API_KEY = os.getenv("ETHERSCAN_API_KEY","GPCB8MUP1RJ2M4GRQSC25N2HD47J34QQ1B")
    # wallet_address = obj.walletAddress

    # Etherscan API URL
    url = f'https://api.etherscan.io/api?module=account&action=balancemulti&address={wallet_address}&tag=latest&apikey={API_KEY}'
    print(url)
    try:
        response = requests.get(url)
        data = response.json()
        print(data)
        if data["status"] == "1":
            return data['result']
        else:
            return "Error fetching balance"
    except Exception as e:
        return f"Error: {str(e)}"
