<?php
class IBSngAPI {
    private $server_url;
    private $username;
    private $password;

    public function __construct($server_url, $username, $password) {
        $this->server_url = rtrim($server_url, '/') . "/IBSng/admin/";
        $this->username = $username;
        $this->password = $password;
    }

    // متد ارسال درخواست به سرور IBSng
    private function sendRequest($action, $params = []) {
        $params['username'] = $this->username;
        $params['password'] = $this->password;
        
        $url = $this->server_url . $action . ".php";
        $post_fields = http_build_query($params);

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $post_fields);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
        
        $response = curl_exec($ch);
        curl_close($ch);

        return json_decode($response, true);
    }

    // 📌 ایجاد اکانت جدید
    public function createAccount($username, $password, $group_name, $credit) {
        return $this->sendRequest("user/add_new", [
            "user_id" => $username,
            "password" => $password,
            "group_name" => $group_name,
            "credit" => $credit,
        ]);
    }

    // 📌 مشاهده اطلاعات اکانت
    public function getAccountInfo($username) {
        return $this->sendRequest("user/info", [
            "user_id" => $username
        ]);
    }

    // 📌 حذف اکانت
    public function deleteAccount($username) {
        return $this->sendRequest("user/delete", [
            "user_id" => $username
        ]);
    }

    // 📌 تغییر میزان اعتبار کاربر
    public function updateCredit($username, $credit) {
        return $this->sendRequest("user/credit_change", [
            "user_id" => $username,
            "credit" => $credit
        ]);
    }

    // 📌 مشاهده وضعیت اتصال کاربران
    public function getActiveUsers() {
        return $this->sendRequest("user/active_list");
    }
}
?>
