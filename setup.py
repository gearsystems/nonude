try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='nonude',
	  version='1.0',
	  description="Avoiding nude images in upload and its detection.",
	  long_description=open('README.md').read(),
      author='GEAR Systems',
      author_email='info@gearsystems.com',
      url='https://github.com/gearsystems/nonude',
      license='',
      platforms='Linux/Mac',
      py_modules=['nude'],
      classifiers=[
          'Development Status :: 1 - Alpha',
          'License :: OSI Approved :: ',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3'],
      keywords="nude",
      zip_safe=False,
      entry_points={'console_scripts': ['nonude = nude:main']},
      )