
# Giới thiệu

Game N - Puzzle là trò chơi cổ điển với nhiều phiên bản và tên gọi khác như : 8 - Puzzle, 15 - Puzzle, ...
Bài toán N - Puzzle là một trong những bài toán điển hình mô phỏng cho các giải thuật tìm kiếm liên quan đến trí tuệ nhân tạo.

# 1. Mục tiêu

- Trạng thái: mỗi trạng thái là một sắp xếp cụ thể vị trí các ô

- Hành động: mỗi hành động tương ứng với một di chuyển ô trống trái, phải, lên, xuống

- Trạng thái xuất phát: được cho trước 

- Trạng thái đích: được cho một cách tường minh

- Giá thành: bằng tổng số lần dịch chuyển ô trống

Lời giải  là chuỗi các hành động cho phép di chuyển từ trạng thái xuất phát tới đích. Lời giải cần ít hành động hơn là lời giải tốt hơn.

# 2. Các thuật toán tìm kiếm

## 2.1. Uniformed Search
Tìm kiếm không có thông tin, còn gọi là tìm kiếm mù (blind, uninformed search) là phương pháp duyệt không gian trạng thái chỉ sử dụng các thông tin theo phát biểu của bài toán tìm kiếm tổng quát trong quá trình tìm kiếm, ngoài ra không sử dụng thêm thông
tin nào khác

- Initial State: Trạng thái ban đầu của 8-puzzle.

- Actions: Các hành động có thể thực hiện (trượt ô trắng lên/xuống/trái/phải).

- Transition Model: Trạng thái mới sau mỗi hành động.

- Goal Test: Kiểm tra xem trạng thái hiện tại có phải trạng thái đích không.

- Path Cost: Chi phí đi từ trạng thái đầu đến trạng thái hiện tại.

Là chuỗi hành động biến trạng thái ban đầu thành trạng thái đích với chi phí thấp nhất (nếu có).

### BFS (Breadth-First Search) – tìm theo bề rộng.

### DFS (Depth-First Search) – tìm theo chiều sâu

### UCS (Uniform Cost Search) – ưu tiên trạng thái có chi phí thấp
BFS ổn định, tìm được lời giải ngắn nhưng tốn bộ nhớ.

DFS nhanh nhưng dễ rơi vào vòng lặp, không đảm bảo lời giải tốt.

UCS tìm đường đi tối ưu nếu chi phí rõ ràng.

IDS tiết kiệm bộ nhớ hơn BFS, nhưng chậm hơn.
### IDS (Iterative Deepening Search) – kết hợp DFS và BFS
Tìm theo DFS những không bao giờ mở rộng các nút có độ sâu quá một giới hạn nào đó. Giới hạn độ sâu được bắt đầu từ 0, sau đó tăng lên 1, 2, 3 v.v. cho đến khi tìm được lời giải.

## 2.2. Informed Search
Chiến lược tìm kiếm có thông tin (Informed search) hay còn được gọi là tìm kiếm heuristic sử dụng thêm thông tin từ bài toán để định hướng tìm kiếm, cụ thể là lựa chọn thứ tự mỏ rộng nút theo hướng mau dẫn tới đích hơn

Hàm f(n) = g(n) + h(n) với:

+ g(n): chi phí từ trạng thái đầu đến trạng thái đang xét

+ h(n): ước lượng chi phí từ trạng thái đang xét đến trạng thái mục tiêu.

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
## 2.5. Constraint Satisfaction Problem (CSP)
Bài toán tìm trạng thái thỏa mãn các ràng buộc (khác với tối ưu đường đi).

▸ Ứng dụng:
Sudoku, lập thời khóa biểu, phân công công việc.

▸ Kỹ thuật:
Backtracking kết hợp với:

Forward Checking

Arc Consistency (AC3)
## 2.6. Reinforcement Learning

Học qua tương tác với môi trường.

Không cần mô hình bài toán, chỉ cần phản hồi (reward).
- Agent
- Environment
- State
- Action
- Reward