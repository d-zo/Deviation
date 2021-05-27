# -*- coding: utf-8 -*-
"""
Deviation.py   v0.2 (2021-05)
"""

# Copyright 2021 Dominik Zobel.
# All rights reserved.
#
# Deviation is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Deviation is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Deviation. If not, see <http://www.gnu.org/licenses/>.


# -------------------------------------------------------------------------------------------------
class Deviation(object):
   def __init__(self, mval=0.0, wcerr=0.0):
      self.mval = mval;
      self.wcerr = wcerr;
   #
   def __repr__(self):
      return str(self.mval) + ' ±' + str(self.wcerr);
   #
   def from_list(self, valuelist):
      from math import sqrt
      #
      temp_list = [];
      for value in valuelist:
         temp_list += [float(value)];
      #
      self.mval = sum(temp_list)/len(temp_list);
      self.wcerr = max([abs(x-self.mval) for x in temp_list]);
   #
   def get_values(self):
      return [self.mval, self.wcerr];
   #
   def _provide_values(self, other_expr):
      if (isinstance(other_expr, Deviation)):
         return other_expr.get_values();
      else:
         return [other_expr, 0.0];
   #
   def _addition(self, other_mval, other_wcerr):
      return [self.mval + other_mval, self.wcerr + other_wcerr];
   #
   def _subtraction(self, other_mval, other_wcerr):
      return [self.mval - other_mval, self.wcerr + other_wcerr];
   #
   def _multiplication(self, other_mval, other_wcerr):
      return [self.mval*other_mval, abs(self.mval)*other_wcerr + abs(other_mval)*self.wcerr + self.wcerr*other_wcerr];
   #
   def _division(self, other_mval, other_wcerr):
      # NOTE: Explicitly handle ((other_mval == 0.0) or (abs(other_mval)-other_wcerr == 0.0))?
      return [self.mval/other_mval, abs((abs(self.mval)+self.wcerr)/(abs(other_mval)-other_wcerr) - abs(self.mval/other_mval))];
   #
   def _power(self, other_mval, other_wcerr):
      # NOTE: Explicitly restrict to real values (self.mval-self.wcerr > 0.0)?
      max_pow = max([(self.mval+self.wcerr)**(other_mval+other_wcerr), (self.mval+self.wcerr)**(other_mval-other_wcerr),
                     (self.mval-self.wcerr)**(other_mval+other_wcerr), (self.mval-self.wcerr)**(other_mval-other_wcerr)]);
      return [self.mval**other_mval, max_pow-self.mval**other_mval];
   #
   def __round__(self, ndigits=None):
      fac = 1;
      if (ndigits is not None):
         fac = 10**ndigits;
      #
      round_mean = round(fac*self.mval)/fac;
      wcerr = self.wcerr + abs(self.mval - round_mean);
      round_wcerr = round(fac*wcerr)/fac;
      round_wcerr_compare = round(10*fac*wcerr)/(10*fac);
      #
      # Increase worst-case error so that the rounded mean value plus/minus the worst-case error still
      # cover all possible values (even if normal rounding rules would round the actual worst-case error down)
      if (round_wcerr < round_wcerr_compare):
         round_wcerr = round(0.5+fac*wcerr)/fac;
      #
      return Deviation(round_mean, round_wcerr);
   #
   def __pos__(self):
      return Deviation(*self.get_values());
   #
   def __neg__(self):
      return Deviation(*self._multiplication(*self._provide_values(other_expr=-1.0)));
   #
   def __add__(self, next_expr):
      return Deviation(*self._addition(*self._provide_values(other_expr=next_expr)));
   #
   def __sub__(self, next_expr):
      return Deviation(*self._subtraction(*self._provide_values(other_expr=next_expr)));
   #
   def __mul__(self, next_expr):
      return Deviation(*self._multiplication(*self._provide_values(other_expr=next_expr)));
   #
   def __truediv__(self, next_expr):
      return Deviation(*self._division(*self._provide_values(other_expr=next_expr)));
   #
   def __pow__(self, next_expr):
      return Deviation(*self._power(*self._provide_values(other_expr=next_expr)));
   #
   def __radd__(self, last_expr):
      return self.__add__(last_expr);
   #
   def __rsub__(self, last_expr):
      temp = Deviation(last_expr);
      return temp.__sub__(self);
   #
   def __rmul__(self, last_expr):
      return self.__mul__(last_expr);
   #
   def __rtruediv__(self, last_expr):
      temp = Deviation(last_expr);
      return temp.__truediv__(self);
   #
   def __rpow__(self, last_expr):
      temp = Deviation(last_expr);
      return temp.__pow__(self);
#
