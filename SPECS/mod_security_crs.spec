Summary: ModSecurity Rules
Name: mod_security_crs
Version: 3.3.4
Release: 3%{?dist}
License: ASL 2.0
URL: https://www.owasp.org/index.php/Category:OWASP_ModSecurity_Core_Rule_Set_Project
Group: System Environment/Daemons
Source: https://github.com/coreruleset/coreruleset/archive/refs/tags/v%{version}.tar.gz
BuildArch: noarch
Requires: mod_security >= 2.8.0
Obsoletes: mod_security_crs-extras < 3.0.0
Patch0: mod_security_crs-early-blocking.patch
Patch1: mod_security_crs-rule-941310-dont-match-japanese-word.patch

%description
This package provides the base rules for mod_security.

%prep
%setup -q -n coreruleset-%{version}
%patch0 -p1 -b.early_blocking
%patch1 -p1 -b.rule_941310

%build

%install

install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules
install -d %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules

# To exclude rules (pre/post)
mv rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
mv rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf

install -m0644 rules/*.conf %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/
install -m0644 rules/*.data %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/
mv crs-setup.conf.example %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/crs-setup.conf

# activate base_rules
for f in `ls %{buildroot}%{_datarootdir}/mod_modsecurity_crs/rules/` ; do 
    ln -s %{_datarootdir}/mod_modsecurity_crs/rules/$f %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules/$f; 
done


%files
%license LICENSE
%doc CHANGES README.md
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/activated_rules/*
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/crs-setup.conf
%{_datarootdir}/mod_modsecurity_crs

%changelog
* Tue Apr 04 2023 Richard Lescak <rlescak@redhat.com> - 3.3.4-3
- bump release to enable build
- Related: rhbz#2040257

* Fri Mar 31 2023 Richard Lescak <rlescak@redhat.com> - 3.3.4-2
- add chained regex for rule 941310 to not match japan word 'company'
- Resolves: rhbz#2040257

* Thu Dec 08 2022 Luboš Uhliarik <luhliari@redhat.com> - 3.3.4-1
- new version 3.3.4
- Resolves: #2141432 - [RFE] upgrade mod_security_crs to latest upstream 3.3.x

* Wed Sep 07 2022 Tomas Korbar <tkorbar@redhat.com> - 3.3.0-5
- Fix application of early blocking patch
- Related: rhbz#2101020

* Mon Sep 05 2022 Tomas Korbar <tkorbar@redhat.com> - 3.3.0-4
- Rebuild because of build system issue
- Related: rhbz#2101020

* Tue Aug 02 2022 Tomas Korbar <tkorbar@redhat.com> - 3.3.0-3
- Backport early blocking feature
- Resolves: rhbz#2101020

* Thu May 06 2021 Lubos Uhliarik <luhliari@redhat.com> - 3.3.0-2
- Resolves: #1855858 - [RFE] update mod_security_crs to 3.3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 22 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-4
- Exclude rule files should not be symlink

* Sat Apr 22 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-3
- Use versioned obsoletes
- Move away from /lib since rules are data

* Sat Apr 22 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-2
- Fix the install part since extra and experimental rules are not longer included in 3.x
- Remove EL5 bits since EL5/EPEL5 are OEL-ed
- Bump reqs

* Sat Apr 22 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0
- Clean up the spec

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.9.20160414git-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 29 2016 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.9.20160414git-1
- Update to 2.9.20160414git

* Tue Mar 08 2016 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.9.20160219git-1
- Update to 2.2.9
- Minor spec cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.8-1
- Update to 2.2.8
- Adapt the spec file to new github tarball schema.
- Correct bugus date in the spec file.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.6-4
- "extras" subpackage is not provided on RHEL7

* Wed Oct 17 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.6-3
- Remove the patch since we're requiring mod_security >= 2.7.0
- Require mod_security >= 2.7.0

* Mon Oct 01 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.6-2
- Add a patch to fix incompatible rules.
- Update to new git release

* Sat Sep 15 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.6-1
- Update to 2.2.6
- Update spec file since upstream moved to Github.

* Thu Sep 13 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.5-5
- Enable extra rules sub-package for EPEL.

* Tue Aug 28 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.5-4
- Fix spec for el5

* Tue Aug 28 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.2.5-3
- Add BuildRoot def for el5 compatibility

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.5-1
- upgrade

* Wed Jun 20 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-3
- "extras" subpackage is not provided on RHEL

* Thu May 03 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-2
- fix fedora-review issues (#816975)

* Thu Apr 19 2012 Peter Vrabec <pvrabec@redhat.com> 2.2.4-1
- initial package


