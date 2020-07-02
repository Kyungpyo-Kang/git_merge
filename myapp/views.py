from django.shortcuts import render, redirect
from .models import Cafe

# 객체의 id를 재정렬하는 메소드
# 목록에서 새로고침을 누르면 실행된다.
def setseq(request):
    # 쿼리셋 메소드를 사용하여 id에 따라서 순서대로 Cafe 타입의 모든 객체를 
    # products 변수에 저장한다.
    products = Cafe.objects.all().order_by('id')
    # 순서에 맞는 id를 부여하기 위해 seq 변수를 선언하고 값을 1로 초기화해준다.
    seq = 1
    
    # 향상된 for문을 활용하여 쿼리셋 타입의 products 변수에 있는 객체들을 하나씩
    # product 변수에 담아서 다음 문장으로 넘겨준다.
    for product in products:

        # product의 id와 seq가 일치하지 않으면 해당 객체의 id가 정렬된 형태가 
        # 아니라는 것을 의미한다.
        if product.id != seq:
            # 쿼리셋 메소드를 활용하여 seq랑 일치하지 않을 때의 id를 가진 product를 
            # 불러오고 그 객체의 id를 seq로 update 해준다.
            # 주의 : 지금은 데이터의 양이 적어서 상관없지만, 데이터 양이 많을 때에는
            # for문 안에서 쿼리셋 메소드를 사용하면 속도가 매우 느려지기 때문에 되도록 일괄처리를 해준다.
            Cafe.objects.filter(id=product.id).update(id=seq)
        # 다음 순번을 위해 seq의 값을 1 증가시킨다.
        seq += 1
    # 위 과정이 끝나면 'show'로 redirect 해줌으로써 다시 show.html로 회귀한다.
    return redirect('show')
        
# id를 초기화하는 메소드
def initseq():
    
    #쿼리셋 메소드를 사용하여 num 변수에 데이터베이스에 저장된 객체의 수를 가져온다.
    num = Cafe.objects.count()

    # num이 0이라는 것은 데이터베이스 안에 객체가 없다는 뜻이므로 seq 변수에 1을 넣어준다.
    if num == 0:
        seq = 1
    # 0이 아니라면
    else:
        # 쿼리셋 메소드를 사용하여 데이터베이스에 저장된 마지막 객체를 product 변수에 저장하고
        # 그 객체의 id에 1을 더한 값을 seq에 저장한다.
        product = Cafe.objects.last()
        seq = product.id + 1

    # 위 작업이 끝나면 seq를 리턴한다. 
    return seq

# 페이지 메인화면을 보여주는 메소드
# 요청(request)를 받으면 index.html로 이동시킨다.
def index(request):
    return render(request, 'index.html')

# 요청을 받으면 상품추가 화면으로 이동시키는 메소드
def create(request):
    return render(request, 'create.html')

# 상품추가 화면 안에 등록! 버튼을 클릭하면 실행되는 메소드
# 등록! 버튼을 클릭함으로써 요청을 보내면 아래와 같은 코드를 실행한다.
def create_pro(request):
    # Cafe() 타입으로 cafe_product를 객체화한다.
    cafe_product = Cafe()
    # 외부(create.html)에서 request.GET을 통해 name=''으로 받아온 값을 
    # 객체의 멤버변수에 저장한다.
    cafe_product.product_name = request.GET['product_name']
    cafe_product.product_price = request.GET['product_price'] 
    # initseq()메소드는 seq를 리턴한다. 메소드 실행결과 리턴된 seq 값으로 객체의 
    # id를 초기화해준다.
    cafe_product.id = initseq()
    # 쿼리셋 메소드 save()를 사용하여 객체의 필드를 데이터베이스에 저장한다.
    cafe_product.save() 

    # 위 과정이 끝나면 다시 메인 화면으로 돌아간다.
    return redirect('index')

# 상품목록을 클릭하면 실행되는 메소드
def show(request):
    # Cafe 테이블을 읽어와서 products라는 변수에 저장한다.
    products = Cafe.objects
    # render로 리턴할 때 3번째 매개변수에 딕셔너리 타입으로 key값에는 임의의 이름(products)을 넣어주고
    # value값에는 앞에서 Cafe 테이블 정보를 저장한 products를 넣어준다.
    # {key:value}
    # 그러면 'show.html'에 해당 딕셔너리 정보와 함께 이동하게 된다.
    return render(request, 'show.html', {'products':products})

# 수정하기 위해 상품을 검색하는 페이지('updateSearch.html')로 이동시켜주는 메소드
# 상품 수정을 클릭하면 실행된다.
def updateSearch(request):
    return render(request, 'updateSearch.html')

# 수정할 상품을 입력하고 검색 버튼을 클릭하면 실행되는 메소드 
def search(request):
    # 입력받은 상품명은 name에 담겨서 여기로 오게된다.
    # 쿼리셋 메소드를 사용하여 입력받은 상품명과 일치하는 객체를 products 변수에 저장한다.
    product = Cafe.objects.filter(product_name=request.GET['product_name'])
    
    # update.html로 product와 함께 이동시킨다.
    # 이때, product는 쿼리셋 타입이므로 [0]을 붙여줌으로써 해당 객체를 돌려주도록 한다.
    return render(request, 'update.html', {'product':product[0]})

# 수정기능을 담당하는 메소드
# 새로운 이름과, 새로운 가격을 입력하고 수정! 버튼을 클릭하면 실행된다.
def update(request):
    # update.html 안에서 hidden type으로 해당 객체의 id를 보냈다.
    # hidden type으로 받아온 객체의 id와 일치하는 객체를 쿼리셋 메소드를 통해 products 변수에 저장한다.
    # 이때 pk(primary_key)는 객체의 id이다.
    # filter를 통해 가져온 데이터는 쿼리셋 타입이므로, [0]번째 인덱스에 있는 객체를 리턴한다.
    product = Cafe.objects.filter(pk=request.GET['product_id'])[0]
    
    # update.html에서 받아온 새로운 상품명과 가격을 해당 객체의 멤버변수에 저장한다.
    product.product_name = request.GET['product_name']
    product.product_price = request.GET['product_price'] 
    
    # 쿼리셋 메소드 save()를 사용하여 기존의 데이터를 덮어씌운다.
    product.save()
    
    #위의 작업이 끝나면 메인화면으로 돌아간다.
    return redirect('index')

# 상품삭제를 클릭하면 실행되는 메소드
# deleteSearch.html로 이동시킨다.
def deleteSeach(request):
    return render(request, 'deleteSearch.html')

# 삭제할 상품명을 입력하고 검색 버튼을 클릭하면 실행되는 메소드
def find(request):
    # deleteSearch에서 받아온 상품명으로 쿼리셋메소드 filter를 사용하여 객체를 찾는다.
    # 이때, 객체의 멤버면수명__contains를 사용하면 받아온 입력값을 포함하는 객체 모두를 리턴한다.
    # 예) '카'를 입력 -> 카푸치노, 카페라떼, 아메리카노 리턴
    # filter를 사용해주었으므로 모델타입으로 리턴
    products = Cafe.objects.filter(product_name__contains=request.GET['product_name']) 
    # 각 객체들을 담아줄 빈 리스트를 product 변수에 저장한다.
    product = []

    # products 안에 들어있는 객체들을 하나씩 꺼내와서 i 변수에 저장하고
    # product 리스트 안에 하나씩 넣어준다.
    for i in products:
        product.append(i)

    # product 리스트를 담아서 'delete.html'로 이동시킨다.
    return render(request, 'delete.html', {'products':product})

# 선택을 하고 삭제버튼을 누르면 실행되는 메소드
def delete(request):
    # delete.html에서 'chk'라는 이름의 변수에 'value='을 통해 해당 상품명을 넣어서 보내주었다.
    # 따라서 request.GET.getlist('chk')를 하게 되면 리스트 형태로 'chk'가 가져온 상품명들을
    # 리턴해준다. 그리고 이를 다시 check_list에 저장한다.

    check_list = request.GET.getlist('chk')

    # 쿼리셋 메소드 filter를 사용하여 조건에 만족하는 객체를 불러온다.
    # 이때, product_name__in을 사용하면 
    # check_list 안에 포함된 상품명들과 일치하는 상품명을 가진 모든 객체들을 리턴한다.
    # 리턴된 객체들을 product 변수에 저장한다.
    product = Cafe.objects.filter(product_name__in=check_list)
    
    # 쿼리셋 메소드 delete()를 사용하여 해당 객체를 데이터베이스에서 삭제한다. 
    product.delete()
    # 위 과정이 정상적으로 이뤄지면 메인 페이지로 돌아간다.
    return redirect('index')

    

