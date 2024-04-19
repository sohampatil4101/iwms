from django.shortcuts import render, HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from rest_framework.generics import GenericAPIView,ListCreateAPIView,ListAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import jwt
from django.contrib.auth import authenticate
from django.conf import settings
import hashlib





# standard functions
def hash_password(password):
    password_bytes = password.encode('utf-8')
    hash_object = hashlib.sha256()
    hash_object.update(password_bytes)
    hashed_password = hash_object.hexdigest()
    
    return hashed_password



def getuserinstance(jwttoken):
    token_data = jwt.decode(jwttoken, "secret", algorithms=['HS256'], do_time_check=True)
    user_id = token_data.get('id')
    user_instance = warehouseuser.objects.get(pk=user_id)
    return user_instance

# Create your views here.


class LoginUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email or password is missing."}, status=status.HTTP_400_BAD_REQUEST)

        user = warehouseuser.objects.filter(email=email, password=hash_password(password)).first()
        print(user,email, password, hash_password(password))
        
        if user is not None:
            payload = {
                "id": user.id,
                "email": user.email,
                "fullname": user.fullname,
                "companyname": user.companyname,
                "phone_no": user.phone_no,
                "country": user.country,
                "state": user.state
            }
            token = jwt.encode(payload, "secret", algorithm='HS256')
            return Response({"Authorization": token}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)








class soham(APIView):
    def post(self, request):
        user_instance = getuserinstance(request.headers.get('Authorization') )
        print("here is the user instance", user_instance)
        user = user_instance
        name = request.data['name']
        so = General.objects.create(user = user, name = name)
        so.save()
        return HttpResponse("done")







from rest_framework.exceptions import ValidationError
from django.db.models import Q

class Registeruser(GenericAPIView):
    serializer_class = warehouseuserSerializer

    def post(self, request):
        # Verify if the same user exists in the database
        email = request.data.get('email')
        phone_no = request.data.get('phone_no')
        companyname = request.data.get('companyname')
        
        if warehouseuser.objects.filter(Q(email=email) | Q(phone_no=phone_no) | Q(companyname=companyname)).exists():
            return Response({"error": "User with the same email, phone number, or company name already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = warehouseuserSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data from serializer
            companyname = serializer.validated_data.get('companyname')
            fullname = serializer.validated_data.get('fullname')
            email = serializer.validated_data.get('email')
            password = hash_password(serializer.validated_data.get('password'))
            phone_no = serializer.validated_data.get('phone_no')
            country = serializer.validated_data.get('country')
            state = serializer.validated_data.get('state')

            # Create user object
            user = warehouseuser.objects.create(
                fullname=fullname,
                companyname=companyname,
                email=email,
                password=password,
                phone_no=phone_no,
                country=country,
                state=state,
            )

            # Generate token for the user
            access_token = RefreshToken.for_user(user)

            # Decode token to extract payload
            try:
                token_data = jwt.decode(str(access_token), options={"verify_signature": False})
            except jwt.ExpiredSignatureError:
                return Response({"error": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
            except jwt.InvalidTokenError:
                return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
            
            payload = {
                "id": user.id,
                "fullname": user.fullname,
                "companyname": user.companyname,
                "email": user.email,
                "mobile": user.phone_no,
                "country": user.country,
                "state": user.state
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            # Construct response data with token
            response_data = {
                "message": "User successfully registered",
                "id": user.id,
                "name": user.companyname + " " + user.fullname,
                "email": user.email,
                "mobile": user.phone_no,
                "country": user.country,
                "state": user.state,
                "token_data": token_data,  # Include decoded token data
                "refresh": str(access_token),
                "access_token": str(access_token.access_token),
                "status_code": status.HTTP_201_CREATED,
                "Authorization": token
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

class Postgstdetails(APIView):
    def post(self, request):
            # Extracting user instance from request headers
            user_instance = getuserinstance(request.headers.get('Authorization'))
            if not user_instance:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # Extracting data from request
            is_business_register_gst = request.data.get('isbuisness_register_gst')
            gstin = request.data.get('gstin')
            gstdate = request.data.get('gstdate')
            composition_scheme = request.data.get('compostion_scheme')
            composition_scheme_percent = request.data.get('compostion_scheme_percent')
            import_export = request.data.get('import_export')
            customduty_tracking = request.data.get('customduty_tracking')
            digital_service = request.data.get('digital_service')
            
            # Creating instance of Gstdetails model
            gstdetails_instance = Gstdetails.objects.create(
                user=user_instance,
                isbuisness_register_gst=is_business_register_gst,
                gstin=gstin,
                gstdate=gstdate,
                compostion_scheme=composition_scheme,
                compostion_scheme_percent=composition_scheme_percent,
                import_export=import_export,
                customduty_tracking=customduty_tracking,
                digital_service=digital_service
            )
            
            # Optionally, you can perform additional validations or operations here
            
            return HttpResponse("done")


class Postadditem(APIView):
    def post(self, request):
        # Extracting user instance from request headers
        user_instance = getuserinstance(request.headers.get('Authorization'))
        if not user_instance:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Extracting data from request
        item_type = request.data.get('item_type')
        # Assuming item_image is uploaded separately
        item_image = request.FILES.get('item_image')
        item_name = request.data.get('item_name')
        item_sku = request.data.get('item_sku')
        item_unit = request.data.get('item_unit')
        item_sac = request.data.get('item_sac')
        returnable_item = request.data.get('returnable_item', False)
        HSN_code = request.data.get('HSN_code')
        taxable = request.data.get('taxable', False)
        exemptional_reason = request.data.get('exemptional_reason')
        sales_info = request.data.get('sales_info', False)
        selling_price = request.data.get('selling_price')
        sales_account = request.data.get('sales_account')
        sales_description = request.data.get('sales_description')
        purchase_info = request.data.get('purchase_info', False)
        cost_price = request.data.get('cost_price')
        purchase_account = request.data.get('purchase_account')
        purchase_description = request.data.get('purchase_description')
        intrastate_tax = request.data.get('intrastate_tax')
        interstate_tax = request.data.get('interstate_tax')
        track_inventory = request.data.get('track_inventory', False)
        inventory_account = request.data.get('inventory_account')
        opening_stock = request.data.get('opening_stock')
        opening_stock_rate_per_unit = request.data.get('opening_stock_rate_per_unit')
        reorder_level = request.data.get('reorder_level')
        preferred_vendor = request.data.get('preferred_vendor')
        dimension = request.data.get('dimension')
        weight = request.data.get('weight')
        manifacturer = request.data.get('manifacturer')
        brand = request.data.get('brand')
        upc = request.data.get('upc')
        mnp = request.data.get('mnp')
        ean = request.data.get('ean')
        isbn = request.data.get('isbn')
        
        # Creating instance of Additem model
        add_item_instance = Additem.objects.create(
            user=user_instance,
            item_type=item_type,
            item_image=item_image,
            item_name=item_name,
            item_sku=item_sku,
            item_unit=item_unit,
            item_sac=item_sac,
            returnable_item=returnable_item,
            HSN_code=HSN_code,
            taxable=taxable,
            exemptional_reason=exemptional_reason,
            sales_info=sales_info,
            selling_price=selling_price,
            sales_account=sales_account,
            sales_description=sales_description,
            purchase_info=purchase_info,
            cost_price=cost_price,
            purchase_account=purchase_account,
            purchase_description=purchase_description,
            intrastate_tax=intrastate_tax,
            interstate_tax=interstate_tax,
            track_inventory=track_inventory,
            inventory_account=inventory_account,
            opening_stock=opening_stock,
            opening_stock_rate_per_unit=opening_stock_rate_per_unit,
            recorder_level=reorder_level,
            preferred_vendor=preferred_vendor,
            dimension=dimension,
            weight=weight,
            manifacturer=manifacturer,
            brand=brand,
            upc=upc,
            mnp=mnp,
            ean=ean,
            isbn=isbn
        )
        
        # Optionally, you can perform additional validations or operations here
        
        return HttpResponse("done")

class PostInventory(APIView):
    def post(self, request):
        # Extracting user instance from request headers
        user_instance = getuserinstance(request.headers.get('Authorization'))
        if not user_instance:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Extracting data from request
        inventory_location = request.data.get('inventory_location')
        fiscal_year = request.data.get('fiscal_year')
        currency = request.data.get('currency')
        language = request.data.get('language')
        inventory_startdate = request.data.get('inventory_startdate')
        
        # Creating instance of Inventory model
        inventory_instance = Inventory.objects.create(
            user=user_instance,
            inventory_location=inventory_location,
            fiscal_year=fiscal_year,
            currency=currency,
            language=language,
            inventory_startdate=inventory_startdate
        )
        
        # Optionally, you can perform additional validations or operations here
        
        return HttpResponse("done")