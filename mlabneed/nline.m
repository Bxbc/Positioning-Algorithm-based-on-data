function[c,ceq]=nline(x)
data1 = cell2mat(struct2cell(load('C:\Users\BC\Desktop\mlabneed\data.mat')));
c=[];
ceq(1)=(x(1)-data1(1,1))^2 + (x(2)-data1(1,2))^2 - x(3)^2;
ceq(2)=(x(1)-data1(1,3))^2 + (x(2)-data1(1,4))^2 - x(3)^2;
ceq(3)=(x(1)-data1(1,5))^2 + (x(2)-data1(1,6))^2 - x(3)^2;
ceq(4)=(x(1)-data1(1,7))^2 + (x(2)-data1(1,8))^2 - x(3)^2;
ceq(5)=(x(1)-data1(1,9))^2 + (x(2)-data1(1,10))^2 - x(3)^2;
ceq(6)=(x(1)-data1(2,1))^2 + (x(2)-data1(2,2))^2 - x(4)^2;
ceq(7)=(x(1)-data1(2,3))^2 + (x(2)-data1(2,4))^2 - x(4)^2;
ceq(8)=(x(1)-data1(2,5))^2 + (x(2)-data1(2,6))^2 - x(4)^2;
ceq(9)=(x(1)-data1(2,7))^2 + (x(2)-data1(2,8))^2 - x(4)^2;
ceq(10)=(x(1)-data1(3,1))^2 + (x(2)-data1(3,2))^2 - x(5)^2;
% ceq(11)=(x(1)-data1(3,3))^2 + (x(2)-data1(3,4))^2 - x(5)^2;
end