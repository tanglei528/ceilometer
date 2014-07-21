INSTALL_ENV=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
[ -d ${INSTALL_ENV}/ceilometer/compute ] || mkdir -p ${INSTALL_ENV}/ceilometer/compute
cp -r /usr/share/ceilometer/ ${INSTALL_ENV}/ceilometer

if [ -f /etc/ceilometer/ceilometer.conf.sample ];then
mv -f /etc/ceilometer/ceilometer.conf.sample /etc/ceilometer/ceilometer.conf
fi
