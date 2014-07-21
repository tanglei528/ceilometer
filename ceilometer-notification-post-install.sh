INSTALL_ENV=`python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()"`
[ -d ${INSTALL_ENV}/ceilometer ] || mkdir ${INSTALL_ENV}/ceilometer
cp /usr/local/*.py ${INSTALL_ENV}/ceilometer/

if [ -f /etc/ceilometer/ceilometer.conf.sample ];then
mv -f /etc/ceilometer/ceilometer.conf.sample /etc/ceilometer/ceilometer.conf
fi
