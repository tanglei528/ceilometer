INSTALL_ENV=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
[ -d ${INSTALL_ENV}/ceilometer ] || mkdir ${INSTALL_ENV}/ceilometer
cp -rf /usr/share/ceilometer/* ${INSTALL_ENV}/ceilometer
if [ -d ${INSTALL_ENV}/ceilometer/alarm ];then
echo "program files cp success"
fi
cp -rf /usr/local/etc/rc.d/init.d/openstack* /etc/init.d/
if [ -d ${INSTALL_ENV}/ceilometer/alarm ];then
echo "service files cp success"
fi
cp /usr/local/etc/rc.d/init.d/* /etc/rc.d/init.d/
[ -d /etc/ceilometer ] || mkdir /etc/ceilometer
cp /usr/local/etc/ceilometer/* /etc/ceilometer
if [ -d /etc/ceilometer ];then
echo "configuration files cp success"
fi

if [ -f /etc/ceilometer/ceilometer.conf.sample ];then
mv -f /etc/ceilometer/ceilometer.conf.sample /etc/ceilometer/ceilometer.conf
fi