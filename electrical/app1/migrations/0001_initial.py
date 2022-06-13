# Generated by Django 4.0.2 on 2022-06-10 12:44

import ckeditor.fields
from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=50, null=True, verbose_name='Full name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('phone_no', models.CharField(max_length=10, null=True, unique=True)),
                ('otp', models.IntegerField(default=False)),
                ('is_used', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(blank=True, max_length=150, null=True, verbose_name='Full Name')),
                ('phone', models.BigIntegerField(blank=True, null=True, verbose_name='Phone Number')),
                ('locality', models.TextField(blank=True, null=True, verbose_name='locality')),
                ('state', models.CharField(blank=True, max_length=100, null=True, verbose_name='State')),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='City')),
                ('pincode', models.BigIntegerField(blank=True, null=True, verbose_name='Pin code')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('home', models.BooleanField(default=False, verbose_name='Home')),
                ('work', models.BooleanField(default=False, verbose_name='Work')),
                ('default', models.BooleanField(default=False, verbose_name='default')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Customer Address',
            },
        ),
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Color', models.CharField(max_length=50, null=True, verbose_name='Color')),
                ('Size', models.CharField(max_length=20, null=True, verbose_name='Size')),
            ],
            options={
                'verbose_name_plural': 'Attributes',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.FileField(blank=True, null=True, upload_to='Banner')),
                ('is_active', models.BooleanField(default=True)),
                ('uploaded_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=150)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brand')),
                ('details', models.TextField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
                ('p_id', models.CharField(blank=True, max_length=5, null=True)),
                ('attributes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.attributes', verbose_name=' Product Attributes')),
            ],
            options={
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=50, null=True, verbose_name='Category')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Category Description')),
                ('category_image', models.ImageField(blank=True, max_length=500, null=True, upload_to='category', verbose_name='Brand Thumbnail')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
            ],
            options={
                'verbose_name_plural': ' Category',
            },
        ),
        migrations.CreateModel(
            name='checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Coupon', models.CharField(blank=True, max_length=100, null=True)),
                ('Shipping_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.address', verbose_name='Shipping Address')),
                ('cart', models.ManyToManyField(to='app1.Cart')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Checkouts',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.CharField(max_length=200, null=True, unique=True, verbose_name='Coupon_code')),
                ('startdate', models.DateField(null=True, verbose_name='Start Date')),
                ('enddate', models.DateField(null=True, verbose_name='End Date')),
                ('coupon_discount', models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Discount(%)')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
            ],
            options={
                'verbose_name_plural': 'Coupons',
            },
        ),
        migrations.CreateModel(
            name='customer_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('Email', models.EmailField(max_length=50, null=True)),
                ('Phone', models.BigIntegerField(null=True)),
                ('Message', models.TextField(max_length=200, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
            ],
            options={
                'verbose_name_plural': 'Customer msgs/contact us',
            },
        ),
        migrations.CreateModel(
            name='enquiryform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Full Name')),
                ('Email', models.EmailField(max_length=50, null=True)),
                ('Phone', models.BigIntegerField(null=True)),
                ('Message', models.TextField(max_length=200, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
            ],
            options={
                'verbose_name_plural': 'FAQ Enquiry',
            },
        ),
        migrations.CreateModel(
            name='image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(blank=True, max_length=255, null=True)),
                ('subscribed_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created date')),
            ],
            options={
                'verbose_name_plural': 'News letter',
            },
        ),
        migrations.CreateModel(
            name='notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offers', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
            ],
            options={
                'verbose_name_plural': 'Notification',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Product Title')),
                ('sku', models.CharField(max_length=255, unique=True, verbose_name='Unique Product ID (SKU)')),
                ('short_description', models.TextField(verbose_name='Short Description')),
                ('detail_description', models.TextField(blank=True, null=True, verbose_name='Detail Description')),
                ('specification', models.TextField(blank=True, null=True, verbose_name='Specification')),
                ('product_image', models.ImageField(blank=True, max_length=500, null=True, upload_to='product', verbose_name='Product Thumbnail')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Price(₹)')),
                ('discounted_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Offer Price(₹)')),
                ('available_stocks', models.CharField(blank=True, max_length=10, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.brand', verbose_name='Product Brand')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.category', verbose_name='Product category')),
                ('image', models.ManyToManyField(blank=True, to='app1.image')),
            ],
            options={
                'verbose_name_plural': '  Products',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign_name', models.CharField(max_length=200, null=True, verbose_name='Campaign name')),
                ('startdate', models.DateField(null=True, verbose_name='Start Date')),
                ('enddate', models.DateField(null=True, verbose_name='End Date')),
                ('sales_discount', models.DecimalField(decimal_places=2, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99)], verbose_name='Discount(%)')),
                ('is_active', models.BooleanField(default=False, verbose_name='Is Active?')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
            ],
            options={
                'verbose_name_plural': 'Sales/Discount',
            },
        ),
        migrations.CreateModel(
            name='socialmedialinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_media', models.CharField(blank=True, max_length=100, null=True, verbose_name='social media')),
                ('links', models.URLField(blank=True, null=True, verbose_name='link')),
            ],
            options={
                'verbose_name_plural': 'Social media links',
            },
        ),
        migrations.CreateModel(
            name='userphoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, default='https://icon2.cleanpng.com/20180319/xrq/kisspng-neck-sitting-line-male-5ab05067ad9d95.1710165615215043597111.jpg', max_length=500, null=True, upload_to='profile', verbose_name='Profle photo')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_category', models.CharField(blank=True, max_length=255, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.category')),
            ],
        ),
        migrations.CreateModel(
            name='redeemed_coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon', models.CharField(blank=True, max_length=50, null=True)),
                ('redeemed_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
                ('checkout_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.checkout', verbose_name='checkout product')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reviews', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('Rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('Status', models.CharField(choices=[('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Approved', 'Approved')], default='Pending', max_length=8, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='app1.product', verbose_name='Product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='ordered Date')),
                ('status', models.CharField(choices=[('ordered', 'ordered'), ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='ordered', max_length=50)),
                ('Shipping_address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.address', verbose_name='Shipping Address')),
                ('checkout_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.checkout', verbose_name='Checked out product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='Price(₹)')),
                ('ordered_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='ordered Date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On The Way', 'On The Way'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=50)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.address', verbose_name='Shipping Address')),
                ('attributes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.attributes', verbose_name=' Product Attributes')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.coupon')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product', verbose_name='Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Order',
            },
        ),
        migrations.CreateModel(
            name='my_account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='Your first name', max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, null=True, verbose_name='last Name')),
                ('phone_number', models.BigIntegerField(null=True, verbose_name='Phone number')),
                ('email', models.EmailField(max_length=255, null=True, verbose_name='Email')),
                ('address', models.TextField(null=True, verbose_name='Address')),
                ('city', models.CharField(max_length=100, null=True, verbose_name='City')),
                ('state', models.CharField(max_length=50, null=True, verbose_name='State')),
                ('is_confirmed', models.BooleanField(default=False)),
                ('otp', models.IntegerField(blank=True, default=False, null=True)),
                ('postal_pin', models.BigIntegerField(null=True, verbose_name='Postal address')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='most_selled_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created date')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
            ],
            options={
                'verbose_name_plural': 'Most selled products',
            },
        ),
        migrations.CreateModel(
            name='MailText',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=255, null=True)),
                ('message', models.TextField(null=True)),
                ('send_it', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created Date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
                ('status', models.CharField(choices=[('d', 'Draft'), ('s', 'sent')], default='d', max_length=1)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Email marketing',
                'verbose_name_plural': 'Email marketing',
            },
        ),
        migrations.CreateModel(
            name='latest_product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='created date')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.product')),
            ],
            options={
                'verbose_name_plural': 'Latest Products',
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.CharField(max_length=100, null=True)),
                ('Answer', ckeditor.fields.RichTextField(max_length=300, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Ordered Date')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated Date')),
                ('status', models.CharField(choices=[('d', 'Draft'), ('p', 'Published'), ('w', 'Withdrawn')], default='d', max_length=1)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.category')),
            ],
            options={
                'verbose_name_plural': 'FAQs',
            },
        ),
        migrations.CreateModel(
            name='cart_order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, null=True, verbose_name='Odered Date')),
                ('product_count', models.CharField(blank=True, max_length=10, null=True)),
                ('total_price', models.IntegerField(blank=True, null=True)),
                ('coupon', models.CharField(blank=True, max_length=10, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('products', models.ManyToManyField(to='app1.Cart')),
                ('shipping_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.address')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app1.product', verbose_name='Product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('detail_description', models.TextField(blank=True, null=True)),
                ('uploaded_date', models.DateField(auto_now_add=True)),
                ('location', models.CharField(blank=True, max_length=50, null=True)),
                ('facebook', models.URLField(null=True)),
                ('instagram', models.URLField(null=True)),
                ('twitter', models.URLField(null=True)),
                ('linkdin', models.URLField(null=True)),
                ('image', models.ManyToManyField(blank=True, to='app1.image')),
            ],
        ),
        migrations.AddField(
            model_name='attributes',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.product', verbose_name='Product'),
        ),
    ]
