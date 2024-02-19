from services.slugify import slugify


class Uploader:

    @staticmethod
    def product_image_uploader(instance, filename):
        return f"products/{instance.product.slug}/{filename}"

    @staticmethod
    def category_image_uploader(instance, filename):
        return f"categories/{slugify(instance.name)}/{filename}"

    @staticmethod
    def review_image_uploader(instance, filename):
        return f"reviews/{instance.user.email}/{filename}"

    @staticmethod
    def notification_image_uploader(instance, filename):
        return f"notifications/{instance.user.email}/{filename}"


