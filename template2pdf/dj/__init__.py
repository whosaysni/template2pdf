# coding: utf-8
 
# Copyright (c) 2010, 2011 Accense Technology, Inc. All rights reserved.
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""PDF renderer, using trml2pdf, for django
"""
import os.path

from django.conf import settings
from django.http import HttpResponse
from django.template import Context, RequestContext, TemplateSyntaxError
from django.template.loader import render_to_string
from django.utils.html import escape
from template2pdf.utils import find_resource_abspath, rml2pdf, FontResolver, ImageResolver


# values from settings
try:
    FONT_DIRS = settings.T2P_FONT_DIRS
except:
    FONT_DIRS = []
try:
    RESOURCE_DIRS = settings.T2P_RESOURCE_DIRS
except:
    RESOURCE_DIRS = []
# populate RESOURCE_DIR with 'resources' under project and application dirs
def populate_resource_dirs(dirs=None, resource_dirname='resources'):
    if dirs==None:
        dirs = [os.path.dirname(os.path.abspath(__file__))]
    for dir_ in dirs:
        path = os.path.join(dir_, resource_dirname)
        if (path not in RESOURCE_DIRS):
            RESOURCE_DIRS.append(path)
populate_resource_dirs()        

# populate FONT_DIRS with RESOURCE_DIRS/fonts
def populate_font_dirs(dirs=RESOURCE_DIRS, font_dirname='fonts'):
    prepends = []
    for dir_ in dirs:
        path = os.path.join(os.path.abspath(dir_), font_dirname)
        if (path not in FONT_DIRS):
            FONT_DIRS.append(path)
populate_font_dirs()        
# font cache
FONT_CACHE = {}

font_resolver = FontResolver(FONT_DIRS, FONT_CACHE).resolve_font
image_resolver = ImageResolver(RESOURCE_DIRS).resolve_image


def render_to_pdf(template_name, params, context_instance=None,
                  font_resolver=font_resolver, image_resolver=image_resolver):
    """Renders PDF from RML, which is rendered from a Django template.

    """
    context_instance = context_instance or Context()
    context_instance.update(params)
    rml = render_to_string(
        template_name, params, context_instance).encode('utf-8')
    try:
        pdf = rml2pdf(rml, font_resolver, image_resolver)
    except Exception, e:
        rml = escape(rml)
        raise TemplateSyntaxError(str(e))
    return pdf


def direct_to_pdf(request, template_name, params=None, context_instance=None,
                  pdf_name=None, download=True):
    """Simple generic view to tender rml template.

    >>> from django.http import HttpRequest
    >>> resp = direct_to_pdf(HttpRequest(), 'common/base.rml')
    >>> resp['content-type'], resp['content-disposition']
    ('application/pdf', 'attachment; filename=base.pdf')
    >>> resp.content[:8]
    '%PDF-1.4'
    """
    context_instance = context_instance or RequestContext(request)
    params = params or {}
    pdf_name = pdf_name or params.pop('pdf_name', None)
    if pdf_name==None:
        tname_body = template_name.rpartition('/')[-1].rpartition('.')[0]
        if tname_body:
            pdf_name = tname_body+'.pdf'
        else:
            pdf_name = 'download.pdf'
    params['pdf_name'] = pdf_name
    pdf = render_to_pdf(template_name, params, context_instance)
    response = HttpResponse(pdf, mimetype='application/pdf')
    if download:
        disposition = 'attachment; filename=%s' %(pdf_name)
        response['Content-Disposition'] = disposition
    return response
