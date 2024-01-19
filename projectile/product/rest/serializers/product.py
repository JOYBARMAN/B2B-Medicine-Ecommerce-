"""Serializers for user product"""

from rest_framework import serializers

from product.models import Product, ProductImages, ProductStock
from shop.models import Shop


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = [
            "id",
            "uid",
            "image",
        ]


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "uid",
            "name",
            "domain",
        ]


class ProductImageAddSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False),
        write_only=True,
    )

    class Meta:
        model = ProductImages
        fields = ["uploaded_images"]

    def create(self, validated_data):
        # Extract uploaded images data from validated_data
        uploaded_images = validated_data.pop("uploaded_images", [])

        # Ectract uid from context and get product
        uid = self.context.get("uid")
        product = Product.objects.get(uid=uid)

        # Create ProductImages instance with product_instance and uploaded images
        post_images = [
            ProductImages(product=product, image=image) for image in uploaded_images
        ]

        # Bulk insert all related objects at once
        created_instances = ProductImages.objects.bulk_create(post_images)

        # Serialize the created instances
        serializer = ProductImagesSerializer(created_instances, many=True)
        serialized_data = serializer.data

        # Return the serialized data
        return serialized_data


class ProductStockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = [
            "id",
            "uid",
            "product",
            "quantity",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "uid",
            "created_at",
            "updated_at",
        ]


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "uid",
            "shop",
            "name",
            "description",
            "price",
            "selling_price",
            "discount",
            "discounted_price",
            "status",
        ]
        read_only_fields = [
            "id",
            "uid",
            "discounted_price",
        ]


class ProductListSerializer(ProductBaseSerializer):
    product_images = ProductImagesSerializer(many=True)
    shop = ShopSerializer(read_only=True)
    product_stock = ProductStockListSerializer(source="productstock")

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + [
            "product_images",
            "product_stock",
        ]
        read_only_fields = ProductBaseSerializer.Meta.read_only_fields + [
            "product_stock",
        ]


class ProductAddSerializer(ProductBaseSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length=None, allow_empty_file=False),
        required=False,
        write_only=True,
    )

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + ["uploaded_images"]
        read_only_fields = ProductBaseSerializer.Meta.read_only_fields + ["shop"]

    def create(self, validated_data):
        shop = Shop.objects.get(domain=self.context.get("domain"))
        # Extract uploaded images data from validated_data
        uploaded_images = validated_data.pop("uploaded_images", [])

        # Create the product instance
        product_instance = Product.objects.create(shop=shop, **validated_data)

        # Create Productmages instance with product_instance and uploaded images
        product_images = [
            ProductImages(product=product_instance, image=image)
            for image in uploaded_images
        ]

        # Bulk insert all related objects at once
        ProductImages.objects.bulk_create(product_images)

        # Serialize the created instance before returning it
        serialized_instance = self.__class__(
            product_instance, context=self.context
        ).data
        return serialized_instance


class ProductDetailSerializer(ProductBaseSerializer):
    product_images = ProductImagesSerializer(many=True)

    class Meta(ProductBaseSerializer.Meta):
        fields = ProductBaseSerializer.Meta.fields + [
            "product_images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ProductBaseSerializer.Meta.read_only_fields + [
            "created_at",
            "updated_at",
        ]
