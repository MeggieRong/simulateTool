
### 情况1 ：有sku，箱规，所属料箱分格，没有库存件数要求

库位仿真原则 ： 100%库位 = 5%空库位 + 95%非空库位
              95%非空库位 先用订单所需sku的库存填充，剩余库位任意填充非订单所需sku库存

代码处理分格的逻辑：
1-> 库存只留下订单所需的sku 

2-> 判断：
  -订单需要的sku都可以在库存找到
  如果有找不到的直接报错，弹出提示 ：订单所需sku在库存不存在，请检查
  -库位是否足够 ：订单所需件数/箱规 = 需要箱子数 <= location的库位数
  如果不足够则直接报错，弹出提示：库位数不够

3-> 只保留订单所需sku，并且通过订单件数/（箱规*50%） = 得到该sku至少所需存储箱子数
  如果箱子数 < 3 ，则变更为3.其余不变
  获取映射表dataFrame sku,binNum,slotType,qty（注意如果qty = 箱规/slotType）

4-> 获取分格类型，比如[1,2,4]

5-> 获取分格库存字典 b = {1: [{skuA: binNum}, {skuB: binNUm}], 
                  2:  [{skuC: binNum}, {skuD: binNUm}],
                  4:  [{skuE: binNum}, {skuF: binNUm}]}
6-> 遍历b ： 
6.1-> 如果是1分格，则直接每个sku都repeat binNum次数,直接insert qty:
      每个箱子编号从1开始

6.2-> 如果是2分格，则直接每个sku都repeat binNum * 2 次数,直接insert qty:
      获取1分格最后的箱子编号n，从n+1开始递增到 repeat binNum + n + 1 号

6.3-> 如果是4分格，则直接每个sku都repeat binNum * 4 次数,直接insert qty:
      获取2分格最后的箱子编号m，从 m + 1 开始递增到 repeat binNum + m + 1 号

6.4-> 得到firstInv

5-> 获取此时订单所需箱子数占库位的百分比a1：
  如果a1 >= 95%，则直接随机从location的ID替换掉箱子编号
  如果a1 < 95%, 则需要生成 (95% - a1)*location个箱子，箱子编号紧跟4分格最后一个编号+1，每个箱子放1件

6-> 合并订单数所需库存及非订单所需库存表，随机从location的ID替换掉箱子编号

### 情况2 ：有sku，箱规，所属料箱分格,有库存件数
1.基本判斷訂單sku是否都可以在庫存中找到
2.基本判斷已提供的庫存件數是否足夠，如果不足夠，通知使用者，已經補齊，最大上限是訂單的總件數
3.根據庫存件數去判斷庫位數是否足夠