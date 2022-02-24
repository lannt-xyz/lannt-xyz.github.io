# Java coding review checklist

## About coding review checklist

Coding rules thì rất quan trọng đối với các lập trình viên vì một số lý do:

- 80% chi phí trọn đời của một phần mềm dành cho bảo trì.
- Hầu như không có phần mềm nào được duy trì trong suốt cuộc đời của tác giả gốc.
- Các quy ước mã cải thiện khả năng đọc của phần mềm, cho phép các kỹ sư hiểu mã mới nhanh hơn và kỹ lưỡng hơn.
- Nếu bạn gửi mã nguồn của mình dưới dạng sản phẩm, bạn cần đảm bảo rằng nó cũng được đóng gói và làm sạch như bất kỳ sản phẩm nào khác mà bạn tạo.

## Checklist

|No.|Checked item|
|:-----|:-----|
|1|Naming rules đã được áp dụng?|
|2|Biến số không sử dụng đã remove?|
|3|Những đoạn code vô nghĩa hoặc không sử dụng đã remove?|
|4|Có dồn quá nhiều xử lý vào 1 method?|
|5|Những đoạn code vô nghĩa đã remove?|
|6|Các xử lý giống nhau đã common hóa và được library hóa?|
|7|Hardcode hoặc code dùng cho debug đã remove?|
|8|Đã xử lý cho trường hợp đối tưởng Null?|
|9|Javadoc đã được ghi đầy đủ?|
|10|Xử lý logic chỉ thể hiện tại domain.model?|
|11|Có dùng for/List?|
|12|Áp dụng SOLID?|
|13|Đã dùng First Class Collection thay cho List?|

### Naming rules

Thống nhất đặt tên class, method, variable, constant

- Dể hiểu
    - Đặt tên dễ hiểu và đúng mục đích, ý nghĩa sử dụng
    - Sử dụng tên biến giống nhau cho các hàm, biến số có cùng mục đích sử dụng, ý nghĩa
    - KHÔNG sai lỗi chính tả
- Format tên class, method, variable
    - Tên class thì đặt theo format UpperCamelCase (PascalCase)
        VD:    AuthorRecommendations
    - Tên variable, method thì đặt theo lowerCamelCase (CamelCase)
        VD:    variable:        memberId
            method:        getUser()
    - Tên biến/tên hàm cho kiểu dữ liệu boolean
        Đối với biến số hoặc hàm số có kiểu dữ liệu là boolean thì sẽ thống nhất theo nguyên tắc bên dưới.
        - can & động từ thể nguyên mẫu
            VD:    canCheckout()
        - has & động từ thể quá khứ
            VD:    hasOrdered()
        - has & danh từ
            VD:    hasOrder()
        - is & tính từ
            VD:    isValid()
        - động từ chia thể hiện tại của danh từ số ít & danh từ
            VD:    existsCart()
    - Tên method trong các class DAO
        - KHÔNG sử dụng dạng số nhiều của danh từ (thêm s, es), hoặc List
            - Lý do: về cơ bản thì hành động get data thì sẽ trả về nhiều record, trong trường hợp chỉ get 1 record thì nên thể hiện thông qua tên method
            - Giải quyết: sử dụng tên method có cấu trúc tương tự như bên dưới, trường hợp cần cách đặt tên khác thì sẽ thảo luận thêm các thành viên trong nhóm
                - selectAll
                - selectById
                - selectOneByAbcXyz
- Tên Hằng số
    - Đặt tên theo SNAKE_CASE
        VD:    MEMBER_ID_LENGTH = 10
    - Tên hằng số thì phải mang ý nghĩa của mục đích sử dụng chứ không phải là thể hiện giá trị của constant đang lưu trữ
        VD:    OK    FILE_PATH_SEPARATOR = "/"
            NG    SLASH = "/"

### Thống nhất trong source code

- Xử lý phải có ý nghĩa
    - Không khai báo những biến số không sử dụng
    Đối với eclipse ide thì những biến số không được sử dụng sẽ được warning, tuy nhiên sau khi hoàn thành coding thì cần confirm lại và xóa đi
    - Không viết những đoạn code vô nghĩa hoặc không được sử dụng
    Trong quá trình thực thi thì có thể sẽ phát sinh những đoạn code tạm và sau khi hoàn thành coding cần confirm lại và xóa đi
- Phân chia xử lý
    - Không dồn quá nhiều xử lý vào một method (mỗi method thực hiện duy nhất một công việc)
    Việc dồn quá nhiều xử lý vào 1 method thì sẽ làm source code thiếu linh động, khó hiểu, dẫn đến khó bảo trì
    - Trường hợp if/else nhiều lần thì nên dùng switch/case
- Thống nhất trong xử lý
    - Các xử lý giống nhau thì phải thực hiện coding giống nhau nhầm dễ review và chỉnh sửa.
- Common hóa
    - Các xử lý giống nhau và được sử dụng lập đi lập lại ở nhiều nơi thì phải làm thành function common dùng chung
- Sử dụng hằng số
    - Không dùng hardcode mà phải khai báo thành hằng số rồi sử dụng
    - Những hằng số mang đặc trưng của một chức năng thì khai báo thành hằng số chỉ sử dụng trong chức năng đó(trong cùng class),
    trường hợp hằng số có thể dùng được ở nhiều chức năng khác nhau thì khai báo thành hằng số common của project
- Xử lý NULL
    - Phải có biện pháp xử lý cho trường hợp đối tượng là NULL
    Trường hợp object NULL thì khi truy cập vào property hoặc method sẽ phát sinh NullPointerException,
      đây là unchecked exception cho nên chỉ khi runtime mới phát sinh, vì vậy nếu không kiểm soát tốt thì sẽ phát sinh bug tìm ẩn
    Khi mà không đảm bảo được object là khác NULL thì cần thêm xử lý check như bên dưới
      if (!ObjectUtils.isEmpty(object)) {
        object.xyz();
      }

### Others

- Comment trong source code	
    - Comment phải được thực hiện đầy đủ, tuy nhiên cũng không nên dư thừa (có những đoạn code đọc vào là có thể hiểu ngay)
	
- Cần đọc qua tài liệu Java Code Conventions từ oracle	
    - https://www.oracle.com/java/technologies/javase/codeconventions-introduction.html#16712
- Ngoài ra cần đọc thêm về Java Style Guide từ google	
    - https://google.github.io/styleguide/javaguide.html
- KHÔNG dùng for mà dùng stream api và các function(map, filter, reduce, collect) của java8
- KHÔNG dùng List để chứa dữ liệu và thao tác trực tiếp trên đó để đảm bảo tính immutable, thay vào đó hãy dùng FirstClassCollection
- KHÔNG thực hiện xử lý logic ở các tầng presentation, infrastructure mà phải đặt đúng xử lý ở các model ở domain
- KHÔNG merge các merge request đang báo lỗi code quality check
- KHÔNG thực hiện khai báo getter, setter hoặc public các properties của object ở tầng model một cách bừa bãi(chỉ khai báo getter khi cần thiết)
- NÊN bao bọc các object có khả năng null bằng Optional và phải có xử lý check ifPresent, isPresent, hoặc orElse, orElseThrow
- NÊN tuân thủ nguyên tắc khi lập trình hướng đối tượng như SOLID, và ứng dụng các design pattern phổ biến như abstract method, abstract factory, dependency injetion
