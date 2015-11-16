try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='nonude',
	  version='1.1.1',
	  description="Avoiding nude images in upload and its detection.",
      author='GEAR Systems',
      author_email='info@gearsystems.com',
      url='https://github.com/gearsystems/nonude',
      license='',
      platforms='Linux/Mac',
      py_modules=['nude'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Internet',
          ],
      keywords="nude",
      zip_safe=False,
      download_url = 'https://github.com/gearsystems/nonude',
      entry_points={'console_scripts': ['nonude = nude:main']},
      )
