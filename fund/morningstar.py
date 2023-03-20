class MorningStar:
    # 名称
    @property
    def css_selector_name(self):
        return ".fundname"

    # 会社
    @property
    def css_selector_comp(self):
        return ".comp"

    # 分類
    @property
    def css_selector_category(self):
        return ".fcate"

    # 基準価額
    @property
    def css_selector_baseprice(self):
        return ".fprice"

    # 直近分配金
    @property
    def css_selector_allotment(self):
        return ".table5b"

    # 買付手数料
    @property
    def css_selector_commision(self):
        return ".table1b"

    # 管理費用率
    @property
    def find_cost(self):
        return "#graph21"

    # 純資産
    @property
    def css_selector_assets(self):
        return ".price2"
