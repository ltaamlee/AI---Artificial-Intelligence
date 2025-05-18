
# Giới thiệu
Game N - Puzzle là trò chơi cổ điển với nhiều phiên bản và tên gọi khác như : 8 - Puzzle, 15 - Puzzle, ...
Bài toán N - Puzzle là một trong những bài toán điển hình mô phỏng cho các giải thuật tìm kiếm liên quan đến trí tuệ nhân tạo.

- Trạng thái: mỗi trạng thái là một sắp xếp cụ thể vị trí các ô
- Hành động: mỗi hành động tương ứng với một di chuyển ô trống trái, phải, lên, xuống
- Trạng thái xuất phát: được cho trước 
- Trạng thái đích: được cho một cách tường minh
- Giá thành: bằng tổng số lần dịch chuyển ô trống. Nói cách khác, mỗi chuyển động có giá thành bằng 1.
Lời giải là chuỗi các hành động cho phép di chuyển từ trạng thái xuất phát tới đích. Lời giải cần ít hành động hơn là lời giải tốt hơn.

# 1. Mục tiêu
- Triển khai các thuật toán tìm kiếm bao gồm: tìm kiếm không thông tin (uninformed), tìm kiếm có thông tin (informed), tìm kiếm cục bộ (local search), tìm kiếm phi quyết định (non-deterministic), bài toán thỏa mãn ràng buộc (constraint satisfaction), học tăng cường (reinforcement learning), cùng với tìm kiếm trong môi trường phức tạp, nhằm giải quyết bài toán 8-puzzle. Mục tiêu giúp người dùng hiểu sâu sắc cơ chế hoạt động cũng như hiệu suất của từng thuật toán.

- Thực hiện phân tích và so sánh chi tiết hiệu quả của các thuật toán dựa trên các tiêu chí như thời gian thực thi, mức sử dụng bộ nhớ, và độ tối ưu của đường đi tìm được qua đó làm nổi bật ưu điểm và hạn chế của từng thuật toán.

- Ngoài ra cung cấp giao diện đồ họa trực quan (GUI) hỗ trợ người dùng dễ dàng theo dõi quá trình giải bài toán 8-puzzle một cách sinh động và trực quan nhất.

# 2. Các thuật toán tìm kiếm

## 2.1. Uniformed Search
Tìm kiếm không có thông tin, còn gọi là tìm kiếm mù (blind, uninformed search) là phương pháp duyệt không gian trạng thái chỉ sử dụng các thông tin theo phát biểu của bài toán tìm kiếm tổng quát trong quá trình tìm kiếm, ngoài ra không sử dụng thêm thông
tin nào khác.

- State Space: Mỗi trạng thái là một cấu hình hợp lệ của bảng 8-puzzle, gồm 8 ô số từ 1 đến 8 và 1 ô trống (ký hiệu là 0).
Tổng số trạng thái hợp lệ là **9! = 362,880**, nhưng chỉ một nửa trong số đó là khả thi (do tính chất hoán vị chẵn/lẻ).
- Initial State: Là cấu hình ban đầu của 9 ô được cung cấp.
- Operators / Actions: Các hành động di chuyển ô trống (0) theo 4 hướng: Trái (Left), Phải (Right), Lên (Up), Xuống (Down). Chỉ hợp lệ nếu không vượt khỏi biên của bảng 3x3.
- Transition Model: Sau khi thực hiện một hành động hợp lệ, ô sẽ chuyển sang trạng thái mới bằng cách hoán đổi ô trống với ô kề bên theo hướng di chuyển.
- Goal State: Là trạng thái sắp xếp đúng thứ tự mà chúng ta muốn 
- Đối với tìm kiếm không thông tin như BFS, DFS, UCS, mỗi hành động thường có chi phí bằng nhau
-> chi phí tổng thường là số bước từ trạng thái ban đầu đến trạng thái đích.
- Solution: Là một danh sách cách trạng thái biểu diễn đường đi từ trạng thái khởi đầu đến trạng thái mục tiêu

### BFS (Breadth-First Search) – tìm theo bề rộng.

### DFS (Depth-First Search) – tìm theo chiều sâu

### UCS (Uniform Cost Search) – ưu tiên trạng thái có chi phí thấp

### IDS (Iterative Deepening Search) – kết hợp DFS và BFS
Phương pháp: Tìm theo DFS những không bao giờ mở rộng các nút có độ sâu quá một giới hạn nào đó. Giới hạn độ sâu được bắt đầu từ 0, sau đó tăng lên 1, 2, 3 v.v. cho đến khi tìm được lời giải.

### So sánh hiệu suất
BFS ổn định, tìm được lời giải ngắn nhưng tốn bộ nhớ.

DFS nhanh nhưng dễ rơi vào vòng lặp, không đảm bảo lời giải tốt.

UCS tìm đường đi tối ưu nếu chi phí rõ ràng.

IDS tiết kiệm bộ nhớ hơn BFS, nhưng chậm hơn.

## 2.2. Informed Search
Chiến lược tìm kiếm có thông tin (Informed search) hay còn
được gọi là tìm kiếm heuristic sử dụng thêm thông tin từ bài toán để định hướng tìm kiếm, cụ thể là lựa chọn thứ tự mỏ rộng nút theo hướng mau dẫn tới đích hơn Thêm yếu tố Heuristic vào đánh giá trạng thái.
- State Space: 
- Initial State:
- Operators / Actions:
- Transition Model:
- Goal State:
- Solution:
- Evaluation Function: Hàm f(n) = g(n) + h(n) với:
g(n): chi phí từ trạng thái đầu đến trạng thái đang xét

h(n): ước lượng chi phí từ trạng thái đang xét đến trạng thái mục tiêu.

### Greedy Best-First Search

### A Search*

### IDA (Iterative Deepening A)**

A* là thuật toán hiệu quả nhất, đảm bảo tìm được lời giải tối ưu nếu heuristic phù hợp.

Greedy nhanh nhưng dễ bỏ qua lời giải tối ưu.

IDA* tiết kiệm bộ nhớ nhưng có thể lặp lại nhiều trạng thái

## 2.3. Local Search

### Simple Hill Climbing

### Steepest-Ascent Hill climbing

### Stochastic Hill Climbing

### Simulated Annealing

### Genetic Algorithm

### Beam Search
Giới hạn beam width - lựa chọn 

## 2.4. Search in Complex Environment
Tìm kiếm trong môi trường phức tạp là một lĩnh vực quan trọng trong trí tuệ nhân tạo, nơi các thuật toán phải đối mặt với nhiều yếu tố không chắc chắn và biến động. Môi trường phức tạp có thể bao gồm nhiều trạng thái, các yếu tố tương tác, và các ràng buộc khó khăn, đòi hỏi các phương pháp tìm kiếm phải linh hoạt và hiệu quả.
Đặc điểm của Môi trường Phức tạp
- Nhiều Trạng thái: Môi trường có thể có hàng triệu trạng thái khác nhau, làm cho việc tìm kiếm trở nên khó khăn hơn.
- Tương tác giữa các yếu tố: Các yếu tố trong môi trường có thể tương tác với nhau, ảnh hưởng đến quyết định và kết quả.
- Tính chắc chắn: Thông tin có thể không đầy đủ hoặc không chính xác, yêu cầu các thuật toán phải xử lý sự không chắc chắn này.
- Thay đổi theo thời gian: Môi trường có thể thay đổi theo thời gian, yêu cầu các thuật toán phải thích ứng nhanh chóng.
### 2.4.1. Non Obser
### 2.4.2. Partial Obser
### 2.4.3. AND-OR Search
Thuật toán đầu vào chỉ cần một trạng thái ban đầu.

- Sử dụng mô hình cây AND-OR, trong đó:

- Nút **AND** đại diện cho các trạng thái cần đồng thời đạt được (tất cả con đều phải đúng).

- Nút **OR** đại diện cho các lựa chọn thay thế (chỉ cần một con đúng).

## 2.5. Constraint Satisfaction Problem (CSP)
Bài toán tìm trạng thái thỏa mãn các ràng buộc (khác với tối ưu đường đi).
- **State Space**: Tập các gán giá trị cho biến thỏa mãn tất cả ràng buộc.
- **Initial State**: Biến chưa được gán giá trị.
- **Operators / Actions**: Gán giá trị hợp lệ cho biến theo thứ tự.
Transition Model: Cập nhật các ràng buộc và loại bỏ các giá trị không phù hợp.
- **Goal State**: Gán giá trị đầy đủ cho các biến thỏa mãn mọi ràng buộc.
- **Solution**: Một tập các giá trị biến thỏa mãn toàn bộ ràng buộc.


## 2.6. Reinforcement Learning
Học qua tương tác trực tiếp với môi trường, không cần biết trước mô hình chuyển đổi trạng thái.
- **Agent**: Thực thể ra quyết định, chọn hành động.
- **Environment**: Môi trường mà agent tương tác.
- **State**: Mô tả tình trạng hiện tại của môi trường.
- **Action**: Hành động agent thực hiện để thay đổi trạng thái.
- **Reward**: Phản hồi ngay sau hành động, dùng để đánh giá hành động đó tốt hay xấu bằng cách cung cấp giá trị số (positive hoặc negative) thể hiện mức độ thành công hoặc thất bại của hành động đó.
Mục tiêu của agent là tối đa hóa tổng phần thưởng nhận được theo thời gian.

