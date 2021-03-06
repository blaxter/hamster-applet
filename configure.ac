AC_INIT([hamster-applet],[2.27.4],[toms.baugis@gmail.com])
AC_CONFIG_SRCDIR(hamster/__init__.py)
AC_CONFIG_HEADERS(config.h)
AC_CONFIG_MACRO_DIR([m4])

AM_INIT_AUTOMAKE([-Wall -Werror foreign])
GNOME_COMMON_INIT

AM_MAINTAINER_MODE
AM_DISABLE_STATIC
AM_PROG_LIBTOOL
AC_SUBST(ACLOCAL_AMFLAGS, "$ACLOCAL_FLAGS -I m4")
AC_PROG_CC

dnl ****************************************************************************
dnl * Pkg-Config
dnl ****************************************************************************
AC_CHECK_PROG(HAVE_PKGCONFIG, pkg-config, yes, no)
if test "x$HAVE_PKGCONFIG" = "xno"; then
  AC_MSG_ERROR(you need to have pkgconfig installed !)
fi

dnl ****************************************************************************
dnl * Translation & i18n
dnl ****************************************************************************

GETTEXT_PACKAGE=hamster-applet
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE, "$GETTEXT_PACKAGE", [Gettext package])
AM_GLIB_GNU_GETTEXT
IT_PROG_INTLTOOL([0.37.1])

dnl ****************************************************************************
dnl * GConf support
dnl ****************************************************************************
AC_PATH_PROG(GCONFTOOL, gconftool-2)
AM_GCONF_SOURCE_2

dnl ****************************************************************************
dnl * Python
dnl ****************************************************************************
AM_PATH_PYTHON(2.4)
AM_CHECK_PYTHON_HEADERS(,[AC_MSG_ERROR(could not find Python headers)])

dnl ****************************************************************************
dnl * Write the values of various paths in defs.py
dnl ****************************************************************************
AC_SUBST(VERSION)
AC_SUBST(PACKAGE)

AS_AC_EXPAND(DATADIR, $datarootdir)
AC_SUBST(DATADIR)

AS_AC_EXPAND(LIBDIR, $libdir)
AC_SUBST(LIBDIR)

AS_AC_EXPAND(PYTHONDIR, $pythondir)
AC_SUBST(PYTHONDIR)
		
dnl ****************************************************************************
dnl * PyGTK & co for Gnome Streamer
dnl ****************************************************************************
PKG_CHECK_MODULES(HAMSTER,
    gtk+-2.0            >= 2.12
    pygtk-2.0           >= 2.12
    pygobject-2.0       >= 2.14
    gnome-python-2.0    >= 2.10

)
AC_SUBST(HAMSTER_CFLAGS)
AC_SUBST(HAMSTER_LIBS)

AC_MSG_CHECKING([for gnomeapplet module])
if AC_RUN_LOG([DISPLAY= $PYTHON -c '
try:
    import pygtk
    pygtk.require("2.0")
    import gtk
    gtk.gdk.threads_init()
    import gnomeapplet
except ImportError, e:
    if str(e).find("gnomeapplet") >= 0:
          raise
except:
    pass
']); then
  AC_MSG_RESULT([yes])
else
  AC_MSG_RESULT([no])
  AC_MSG_ERROR([gnomeapplet Python module required to build hamster])
fi

dnl ****************************************************************************
dnl * PyGTK Codegen and defs files
dnl ****************************************************************************
AC_PATH_PROG(PYGTK_CODEGEN, pygtk-codegen-2.0, no)
if test "x$PYGTK_CODEGEN" = xno; then
  AC_MSG_ERROR(could not find pygtk-codegen-2.0 script)
fi

AC_MSG_CHECKING(for pygtk defs)
PYGTK_DEFSDIR=`$PKG_CONFIG --variable=defsdir pygtk-2.0`
AC_SUBST(PYGTK_DEFSDIR)
AC_MSG_RESULT($PYGTK_DEFSDIR)


if test "x$PYTHON_VERSION" = "x2.4"; then
    AC_MSG_CHECKING([for pysqlite2 module])
    if AC_RUN_LOG([DISPLAY= $PYTHON -c '
try:
    import pysqlite2
except ImportError, e:
    if str(e).find("pysqlite2") >= 0:
        raise
except:
    pass
    ']); then
      AC_MSG_RESULT([yes])
    else
      AC_MSG_RESULT([no])
      AC_MSG_ERROR([Python 2.4: pysqlite2 module required to build hamster])
    fi
else
    AC_MSG_CHECKING([for python sqlite module])
    if AC_RUN_LOG([DISPLAY= $PYTHON -c '
try:
    import sqlite3
except ImportError, e:
    if str(e).find("sqlite3") >= 0:
        raise
except:
    pass
    ']); then
      AC_MSG_RESULT([yes])
    else
      AC_MSG_RESULT([no])
      AC_MSG_ERROR([Python 2.5+: inbuilt sqlite is required to build hamster])
    fi
fi



dnl ==========================
dnl Control-Center Keybindings
dnl ==========================

AC_MSG_CHECKING([whether the GNOME control-center supports custom keybindings])
if $PKG_CONFIG --variable=keysdir gnome-keybindings > /dev/null; then
    AC_MSG_RESULT([yes])
    KEYBINDINGS_DIR="`$PKG_CONFIG --variable=keysdir gnome-keybindings`"
    AC_SUBST(KEYBINDINGS_DIR)
else
    AC_MSG_RESULT([no])
    KEYBINDINGS_DIR=""
fi
AM_CONDITIONAL([CUSTOM_KEYBINDINGS],[test -n "$KEYBINDINGS_DIR"])


dnl ****************************************************************************
dnl * --------------------------------------------------------------------------
dnl ****************************************************************************
AC_CONFIG_FILES([
Makefile
hamster/Makefile
hamster/defs.py
hamster/keybinder/Makefile
data/Makefile
data/art/Makefile
po/Makefile.in
])
AC_OUTPUT

echo
echo $PACKAGE v$VERSION
echo

echo Prefix............... : $prefix

echo "Now type make to compile"
echo "Then su to root and type: make install"
echo
