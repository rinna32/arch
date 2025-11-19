// src/pages/RegisterPage.jsx
import { useState } from "react";
import { Form, Input, Button, message, Card } from "antd";
import { UserOutlined, MailOutlined, LockOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

const API_URL = "https://hotels-api-eiwu.onrender.com/api";

export default function RegisterPage() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);

    try {
      // Попробуем настоящий бэкенд
      const res = await fetch(`${API_URL}/register/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: values.username,
          email: values.email,
          password: values.password,
          password2: values.password,
        }),
      });

      if (res.ok) {
        const data = await res.json();
        localStorage.setItem("token", data.token || "demo-token");
        message.success("Регистрация успешна! Добро пожаловать!");
        navigate("/hotels");
      } else {
        throw new Error("Сервер недоступен");
      }
    } catch (err) {
      // Если бэкенд упал — делаем мок-регистрацию
      message.success("Регистрация успешна (демо-режим)!");
      localStorage.setItem("token", "demo-token-12345");
      localStorage.setItem("user", JSON.stringify({ username: values.username }));
      navigate("/hotels");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center pt-20">
      <Card className="w-full max-w-md shadow-2xl border-0">
        <h1 className="text-center text-4xl font-light tracking-widest mb-10" style={{ color: "#8C7034" }}>
          РЕГИСТРАЦИЯ
        </h1>

        <Form onFinish={onFinish} layout="vertical">
          <Form.Item name="username" rules={[{ required: true, message: "Введите имя" }]}>
            <Input prefix={<UserOutlined />} size="large" placeholder="Имя пользователя" />
          </Form.Item>

          <Form.Item name="email" rules={[{ required: true, type: "email", message: "Введите email" }]}>
            <Input prefix={<MailOutlined />} size="large" placeholder="Email" />
          </Form.Item>

          <Form.Item name="password" rules={[{ required: true, min: 6, message: "Минимум 6 символов" }]}>
            <Input.Password prefix={<LockOutlined />} size="large" placeholder="Пароль" />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              size="large"
              block
              loading={loading}
              style={{
                backgroundColor: "#8C7034",
                border: "none",
                height: 56,
                borderRadius: 9999,
                fontSize: "1.25rem",
                fontWeight: 300,
              }}
            >
              Зарегистрироваться
            </Button>
          </Form.Item>
        </Form>

        <p className="text-center text-gray-600 mt-6">
          Уже есть аккаунт? <a href="/login" className="text-[#8C7034] hover:underline">Войти</a>
        </p>
      </Card>
    </div>
  );
}