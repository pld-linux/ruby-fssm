#
# Conditional build:
%bcond_without	tests		# build without tests

%define pkgname fssm
Summary:	File system state monitor
Name:		ruby-%{pkgname}
Version:	0.2.10
Release:	2
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	84c339af7eec2b408c757be5912579a8
URL:		http://github.com/ttilley/fssm
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.665
%if %{with tests}
BuildRequires:	rubygem(rspec)
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The File System State Monitor keeps track of the state of any number
of paths and will fire events when said state changes
(create/update/delete). FSSM supports using FSEvents on MacOS (with
ruby 1.8), Inotify on GNU/Linux, and polling anywhere else.

%package doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -n %{pkgname}-%{version}

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
# Remove Bundler dependency
sed -i '/bundler\/setup/d' spec/spec_helper.rb

rspec spec/
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{ruby_vendorlibdir}
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.markdown example.rb
%{ruby_vendorlibdir}/fssm.rb
%{ruby_vendorlibdir}/fssm
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
