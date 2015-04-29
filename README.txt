==============================================
template2pdf: Converts tRML template to PDF
==============================================

**IMPORTANT: Kay support will be dropped.**

Great thanks to:
* The !ReportLab Project, for providing handy PDF interface to Python: http://www.reportlab.com/
* Favien Pinckaers of OpenERP, the original author of trml2pdf code.
* Rohit Sankaran, owner of !GitHub trml2pdf master: http://github.com/roadhead/trml2pdf/
* Taniguchi Takaki, for early mention of trml2pdf in Japan: http://takaki-web.media-as.org/blog/ 

Usage
======

Writing tRML with template markups
-------------------------------------

<!DOCTYPE document SYSTEM "rml.dtd">
{% load pdf_tags %}
<document filename="{{ pdf_name }}">
  {% block template %}
  <template pagesize="({% block pagesize %}595, 841{% endblock %})" 
	    showBoundary="0">
    {% block template_content %}
    <pageTemplate id="main">
      {% block page_graphics %}
      <pageGraphics>
	{% block header %}
	{% endblock header %}
	{% block footer %}
	{% endblock footer %}
      </pageGraphics>
      {% endblock page_graphics %}
      {% block frame %}
      <frame id="content"
	     x1="{{ content_x1|default:"40" }}"
	     y1="{{ content_y1|default:"60" }}"
	     width="{{ content_width|default:"515" }}"
	     height="{{ content_height|default:"710" }}"/>
      {% endblock frame %}
      {% block extra_frames %}
      {% endblock extra_frames %}
    </pageTemplate>
    {% endblock template_content %}
  </template>
  {% endblock template %}
  {% block stylesheet %}
  <stylesheet>
    {% block styles %}
    <paraStyle name="Normal"
	       fontName="{% firstof normal_font_name font_name "Serif" %}"
	       fontSize="{% firstof normal_font_size font_size|default:"9" %}"
	       textColor="{% firstof normal_text_color text_color "black" %}"
	       wordWrap="CJK"
	       />
    {% endblock styles %}
    {% block extra_styles %}
    {% endblock extra_styles %}
  </stylesheet>
  {% endblock stylesheet %}
  {% block story %}
  <story>
    {% block story_content %}
    {% block content %}
    <para style="Normal">
      This is main content
    </para>
    {% endblock content %}
    {% endblock story_content %}
  </story>
  {% endblock story %}
</document>


Note:
* As normal Django templates, inheritance, filters, tags are available.
* Unfortunately tRML does not support cross references.

Rendering in a view
----------------------

# coding: utf-8

from template2pdf.dj import direct_to_pdf

def myview(request, template_name='somewhere/yourtemplate.rml'):
    params = {}
    # ... populate params in your order.
    return direct_to_pdf(request, template_name, params)

Hints:
* Setting Content-Disposition will tell your browser to download content as a file, instead of opening in it.
