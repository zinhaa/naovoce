from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django import forms

from modeltranslation.admin import TranslationAdmin

from gallery.admin import ImageAdminInline, GalleryAdminMixin
from gallery.forms import CoverImageAdminForm
from .models import Kind, Fruit
from .herbarium.models import Herbarium


class KindModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['key'] = self.instance.strkey


class KindAdmin(TranslationAdmin):
    fields = 'cls name color key'.split()
    list_display = 'name _class _color _fruit_count key'.split()

    def _class(self, obj):
        return obj.CLS.text_of(obj.cls)
    _class.short_description = _('class')
    _class.admin_order_field = 'cls'

    def _color(self, obj):
        color_html = '<div class="cbox" style="background:#{color}"></div> #{color}'
        return color_html.format(color=obj.color)
    _color.short_description = _('color')
    _color.allow_tags = True

    def _fruit_count(self, obj):
        return obj.fruits.count()
    _fruit_count.short_description = _('markers count')


class FruitAdmin(GalleryAdminMixin, admin.ModelAdmin):
    fields = 'latitude longitude kind description user deleted why_deleted cover_image'.split()
    list_display = 'id __str__ latitude longitude user deleted images_count created'.split()
    list_filter = 'kind__name_cs deleted'.split()
    search_fields = 'id user__username user__email'.split()
    form = CoverImageAdminForm
    inlines = ImageAdminInline,

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()


class HerbariumAdmin(admin.ModelAdmin):
    model = Herbarium
    list_display = 'kind full_name latin_name'.split()


admin.site.register(Herbarium, HerbariumAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(Fruit, FruitAdmin)
