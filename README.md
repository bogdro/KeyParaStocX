# KeyParaStocX #

KeyParaStocX (Keyword-based Paragraph Styling and Table of Contents eXtension)
is a LibreOffice/Apache OpenOffice/OpenOffice.org extension that searches for
the configured keywords in a text, changes their style and builds a Table of
Contents for them.

The extension was formerly called "Pożeracz ustaw" or "PozeraczUstaw".

Requirements: a compatible office suite:

-   LibreOffice (<https://www.libreoffice.org/>)
-   Apache OpenOffice (<https://www.openoffice.org/>)
-   the old OpenOffice.org

Author: Bogdan Drozdowski, bogdro (at) users . sourceforge . net

License: GNU GPL version 3 or newer.

See the `INSTALL` file for installation instructions.

Project homepage: <https://keyparastocx.sourceforge.io/>

[![SonarQube Cloud](https://sonarcloud.io/images/project_badges/sonarcloud-light.svg)](https://sonarcloud.io/summary/new_code?id=bogdro_KeyParaStocX)

## Usage ##

Running with the default settings:

1.  Open the Writer application of the office suite.
2.  Open a document you wish to transform.
3.  Click the KeyParaStocX icon (the same as the project icon) on the toolbar,
    right after the "Toggle Formatting Marks" icon in the spellchecking
    toolbar (see the project screenshots), or choose the `Tools`
    menu, then `Add-Ons` and `KeyParaStocX`.
4.  Wait until a message box saying "OK" is displayed.

## Configuration ##

Configuring the extension:

1.  Open the Writer application of the office suite.
2.  Choose the `Tools` menu and then `Options...`.
3.  Expand `Writer` section on the left (e.g. "LibreOffice Writer").
4.  Click "KeyParaStocX - options".
5.  Set the keywords/regular expressions you wish KeyParaStocX to recognize
	and the styles you wish they should get.
6.  Click "OK".

If you get an error message when running the extension, check the spelling
of your styles.

In some office suites, you may need to use the English names for the styles,
i.e. "Heading 1" to "Heading 7".

## Compatibility ##

Various versions of KeyParaStocX have been successfully used with the
following applications in the following versions:

1.  LibreOffice:
-   7.x (checked: 7.5.0.3, 7.6.1.2)
-   24.x (checked: 24.2.3.2, 24.8.2.1)
-   25.x (checked: 25.2.0.3)

2.  Apache OpenOffice:
-   4.x (checked: 4.1.13, 4.1.14)

3.  OpenOffice.org:
-   3.x (checked: 3.3 probably)

Other versions may also work.

## ChangeLog ##

For a list of changes, refer to the `ChangeLog` file in the package.

## WARNING ##

The `dev` branch may contain code which is a work in progress and committed just for tests. The code here may not work properly or even compile.

The `master` branch may contain code which is committed just for quality tests.

The tags, matching the official packages on SourceForge, should be the most reliable points.
