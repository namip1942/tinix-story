import json

DESC_MAP = {
    "Xuyên không": "Nhân vật chính từ thế giới thực xuyên đến một thế giới khác, thời đại khác.",
    "Xuyên sách": "Nhân vật chính xuyên vào cốt truyện của một bộ tiểu thuyết, thường thay đổi số phận của nguyên chủ.",
    "Trọng sinh": "Nhân vật chính chết đi và sống lại ở một thời điểm trong quá khứ để làm lại cuộc đời.",
    "Hệ thống": "Được gắn kết với một hệ thống (trí tuệ nhân tạo) cung cấp nhiệm vụ, kỹ năng và đạo cụ.",
    "Bàn tay vàng": "Sở hữu năng lực, bảo bối hoặc lợi thế cực kỳ to lớn ngay từ đầu.",
    "Không gian tùy thân": "Có một dị không gian bí mật để tàng hình, lưu trữ vật phẩm hoặc trồng trọt.",
    "Linh tuyền": "Sở hữu suối nước thánh có tác dụng cường thân kiện thể, chữa bách bệnh, thúc đẩy sinh trưởng.",
    "Đọc tâm thuật": "Năng lực ngoại cảm có thể nghe được suy nghĩ thực sự của người khác.",
    "Vô địch lưu": "Nhân vật chính sở hữu sức mạnh vô địch, áp đảo mọi kẻ thù ngay từ đầu truyện.",
    "Cẩu đạo": "Nhân vật chính theo trường phái ẩn nhẫn, phát triển âm thầm, tuyệt đối không phô trương để giấu thực lực.",
    "Nhiệt huyết": "Mạch truyện sục sôi, đề cao tinh thần chiến đấu không lùi bước, dũng cảm đối mặt rủi ro.",
    "Hài hước": "Văn phong mang đậm tính giải trí, tấu hài, nhiều tình huống dở khóc dở cười.",
    "Sảng văn": "Truyện tập trung vào sự thăng tiến nhanh chóng, vả mặt kẻ khinh thường mình, mang lại cảm giác thỏa mãn.",
    "Ngọt sủng": "Tình tiết lãng mạn, ngọt ngào, nhân vật chính được yêu thương chiều chuộng hết mực, ít bi kịch.",
    "Ngược luyến": "Tình yêu nhiều oán hận, hiểu lầm, dằn vặt tổn thương sâu sắc cả thể xác lẫn tinh thần.",
    "Gương vỡ lại lành": "Hai người từng yêu nhau, chia tay vì hiểu lầm hoặc hoàn cảnh, sau đó vượt qua thử thách để quay về bên nhau.",
    "Cưới trước yêu sau": "Kết hôn vì bổn phận, giao dịch hoặc ép buộc, sau quá trình sống chung mới nảy sinh tình cảm thật sự.",
    "Oan gia ngõ hẹp": "Cặp đôi ban đầu có ấn tượng xấu, ghét bỏ nhau, nhưng qua nhiều đụng độ lại dần yêu nhau.",
    "Thanh mai trúc mã": "Nhân vật lớn lên cùng nhau từ nhỏ, có nền tảng tình cảm gắn kết sâu đậm và hiểu rõ về nhau.",
    "Hào môn thế gia": "Bối cảnh giới siêu giàu, gia tộc quyền thế, đi kèm với tranh giành tài sản hoặc hôn nhân thương mại.",
    "Tổng tài": "Nam chính là giám đốc, chủ tịch bá đạo, quyền thế, lạnh lùng nhưng rất sủng ái nữ chính.",
    "Minh tinh": "Nhân vật chính là ngôi sao giải trí, cốt truyện khai thác ánh hào quang và góc khuất của showbiz.",
    "Giới giải trí": "Bối cảnh tập trung vào mâu thuẫn, lịch trình, scandal và hoạt động nghệ thuật của giới giải trí.",
    "Vườn trường": "Truyện xoay quanh cuộc sống thanh xuân học đường, tình cảm tuổi học trò trong sáng và nhiệt huyết.",
    "Học bá": "Nhân vật chính có trí tuệ xuất chúng, tính toán thần sầu, giỏi giang về mặt học vấn.",
    "Võng du": "Nhân vật chơi game online (có thể là thực tế ảo), cốt truyện đan xen giữa game và đời thực.",
    "E-sports": "Tập trung vào thể thao điện tử chuyên nghiệp, giải đấu và sự cạnh tranh khốc liệt khao khát cúp vô địch.",
    "Livestream": "Sử dụng hình thức phát sóng trực tiếp (livestream) để tương tác, kiếm tiền hoặc làm nhiệm vụ.",
    "Mỹ thực": "Tập trung miêu tả các món ăn ngon, quá trình nấu nướng và kinh doanh nhà hàng xuất sắc.",
    "Nông trại": "Quản lý và phát triển nông trại, thường kết hợp với kinh tế nhàn nhã, chữa lành.",
    "Điền văn": "Cốt truyện bình dị, mô tả cuộc sống làm ruộng, làm nông trồng trọt chăn nuôi mang hơi thở dân dã, ấm cúng.",
    "Nuôi con": "Tập trung vào hành trình chăm sóc, nuôi dưỡng con cái (con ruột, con nuôi hoặc manh bảo).",
    "Làm giàu": "Quá trình nhân vật chính từ hai bàn tay trắng xây dựng sự nghiệp, kinh doanh trở nên giàu sang phú quý.",
    "Cung đấu": "Những mưu mô ác hiểm tranh giành sủng ái và quyền lực chốn hậu cung giữa các phi tần.",
    "Gia đấu": "Xung đột lợi ích, quyền hành và địa vị nội bộ trong các đại gia tộc danh gia vọng tộc.",
    "Quyền mưu": "Sử dụng trí mưu, âm mưu quyền thuật thâm sâu để tranh đoạt vương quyền, vị thế trên triều đình.",
    "Nữ cường": "Nữ chính độc lập, mạnh mẽ, thông minh, không quá luỵ nam chính, thường tự giải quyết các rắc rối mưu mô.",
    "Nam cường": "Nam chính vô cùng mạnh mẽ, quyền thế, tài giỏi, cường giả vi tôn che chở và bảo vệ người mình yêu.",
    "Song khiết": "Cả nam và nữ chính đều là mối tình đầu tiên về cả thể xác lẫn tâm hồn của nhau, 1v1 tuyệt đối.",
    "Phế Sài": "Nhân vật chính bị coi là đồ bỏ đi, rác rưởi, không có tài năng bẩm sinh nhưng sau đó quật khởi vả mặt.",
    "Thiên tài": "Có năng khiếu phi phàm vượt trội, thiên phú cực cao, tốc độ tu luyện hoặc tiếp thu nhanh hơn bất kỳ ai.",
    "Mỹ cường thảm": "Nhân vật có ngoại hình đẹp, thực lực siêu cường cực hạn nhưng mang quá khứ hoặc số phận bi thương.",
    "Trà xanh": "Nhân vật nữ bề ngoài tỏ ra yếu đuối, ngây thơ thánh thiện nhưng tâm can đầy mưu mô ly gián hạ bệ người khác.",
    "Bạch liên hoa": "Có ý nghĩa tương tự Trà xanh, bề ngoài băng thanh ngọc khiết thiện lương nhưng tâm tính hèn mọn, tính toán thâm sâu.",
    "Hắc hóa": "Nhân vật từ phe chính nghĩa thiện lương vì quá đau khổ tuyệt vọng mà chuyển biến sang tàn nhẫn, ác độc, không thủ đoạn.",
    "Cứu rỗi": "Một người đang trong tăm tối, đau khổ được người kia bao dung thông qua tình yêu mang về với ánh sáng hy vọng.",
    "Chữa lành": "Văn phong ấm áp ngọt ngào, nhấn mạnh vào quá trình các nhân vật xoa dịu vết thương lòng hoặc áp lực cuộc sống cho nhau.",
    "Manh bảo": "Trẻ con đáng yêu, thông minh lanh lợi, đóng vai trò trợ tâm cho cha mẹ xích lại gần nhau.",
    "Hậu cung": "Nhân vật chính (thường là nam) có mối quan hệ tình cảm đồng thời và kết hôn cùng nhiều nhân vật khác giới.",
    "1v1": "Cốt truyện chỉ xoay quanh tình yêu duy nhất trọn đời giữa hai người, thủy chung 1 nam - 1 nữ.",
    "NP": "Motif Poly (Multiple Partners), một nhân vật chính có mối quan hệ tình cảm lãng mạn chính thức với nhiều người cùng một lúc và kết thúc có hậu cùng nhau hòa bình.",
    "Dị thế": "Xuyên đến một thế giới hoàn toàn khác Trái Đất, với những hệ tư tưởng, ma pháp hay nền văn minh dị thường."
}

path = r"c:\Users\lupan\Desktop\Workspace\AIStudioWorkspace\tinix-story\services\data\sub_genres.json"
default_desc = "AI sẽ sử dụng quy chuẩn và đặc trưng của thể loại con này để tối ưu hóa tình tiết, bối cảnh và văn phong câu chuyện."

try:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        name = item["name"]
        if not item.get("description") or item["description"].strip() == "":
            item["description"] = DESC_MAP.get(name, default_desc)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Done generating Sub Genre descriptions.")
except Exception as e:
    print(f"Error: {e}")
