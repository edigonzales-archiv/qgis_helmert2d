# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Helmert2D
                                 A QGIS plugin
 Helmert2D transformation
                             -------------------
        begin                : 2014-06-09
        copyright            : (C) 2014 by Stefan Ziegler
        email                : edi.gonzales@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Helmert2D class from file Helmert2D.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .helmert2d import Helmert2D
    return Helmert2D(iface)
