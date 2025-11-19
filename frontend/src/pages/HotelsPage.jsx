import { useLocation } from "react-router-dom";
import { useState } from "react";
import { Modal, Form, DatePicker, InputNumber, Button, message } from "antd";
import { UserOutlined } from "@ant-design/icons";
import axios from "axios";
import dayjs from "dayjs";

const API_URL = "https://hotels-api-eiwu.onrender.com/api";

export default function HotelsPage() {
  const { state } = useLocation();
  const hotel = state?.hotel;

  const [selectedRoom, setSelectedRoom] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();

  if (!hotel) {
    return (
      <div className="pt-32 text-center text-4xl font-light text-red-600">
        Отель не найден
      </div>
    );
  }

  const openBookingModal = (room) => {
    setSelectedRoom(room);
    setIsModalOpen(true);
  };

  const handleBooking = async (values) => {
    const token = localStorage.getItem("token");
    if (!token) {
      message.warning("Войдите в аккаунт для бронирования");
      return;
    }

    try {
      await axios.post(
        `${API_URL}/bookings/`,
        {
          room_type: selectedRoom.id,
          check_in: values.dates[0].format("YYYY-MM-DD"),
          check_out: values.dates[1].format("YYYY-MM-DD"),
          guests: values.guests,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      message.success("Бронь успешно создана!");
      setIsModalOpen(false);
      form.resetFields();
    } catch (err) {
      const msg = err.response?.data
        ? Object.values(err.response.data).flat()[0]
        : "Ошибка бронирования";
      message.error(msg);
    }
  };

  return (
    <div className="pt-32 pb-20 px-4 md:px-8 lg:px-16 max-w-7xl mx-auto">
      <h1 className="text-center text-4xl md:text-5xl font-light tracking-widest mb-12" style={{ color: "#8C7034" }}>
        {hotel.name.toUpperCase()}
      </h1>

      {/* Главное фото отеля */}
      <div className="mb-16 flex justify-center">
        <img
          src={`https://picsum.photos/1200/600?random=${hotel.id}`}
          alt={hotel.name}
          className="rounded-3xl shadow-2xl max-w-full h-auto max-h-96 object-cover"
        />
      </div>

      {/* Описание */}
      <div className="mb-20">
        <p className="text-center text-lg md:text-xl font-light text-gray-700 leading-relaxed max-w-4xl mx-auto bg-white/70 backdrop-blur-sm py-8 px-12 rounded-3xl shadow-lg">
          {hotel.description || "Эксклюзивный отель премиум-класса с потрясающими видами и высочайшим уровнем сервиса."}
        </p>
      </div>

      <h2 className="text-center text-4xl md:text-5xl font-light tracking-widest mb-16" style={{ color: "#8C7034" }}>
        TYPES OF ROOMS
      </h2>

      {/* Номера */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
        {hotel.room_types.map((room) => (
          <div key={room.id} className="group cursor-pointer" onClick={() => openBookingModal(room)}>
            <div className="overflow-hidden rounded-3xl shadow-2xl mb-6">
              <img
                src={`https://picsum.photos/800/600?random=${room.id}`}
                alt={room.name}
                className="w-full h-80 object-cover group-hover:scale-105 transition duration-500"
              />
            </div>
            <div className="text-center">
              <span className="inline-block bg-[#8C7034] text-white px-8 py-3 rounded-full text-lg font-light tracking-widest">
                {room.name.toUpperCase()}
              </span>
              <p className="mt-4 text-gray-600">
                до {room.capacity} гостей • {room.price_per_night} ₽ / ночь
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Модалка бронирования */}
      <Modal
        open={isModalOpen}
        onCancel={() => setIsModalOpen(false)}
        footer={null}
        width={600}
        title={<span style={{ color: "#8C7034", fontSize: "1.8rem", fontWeight: 300 }}>{selectedRoom?.name}</span>}
      >
        <Form form={form} layout="vertical" onFinish={handleBooking}>
          <Form.Item name="dates" label="Даты" rules={[{ required: true }]}>
            <DatePicker.RangePicker
              size="large"
              className="w-full"
              format="DD.MM.YYYY"
              disabledDate={(d) => d && d < dayjs().startOf("day")}
            />
          </Form.Item>

          <Form.Item name="guests" label="Гостей" initialValue={1}>
            <InputNumber min={1} max={selectedRoom?.capacity} className="w-full" prefix={<UserOutlined />} />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              size="large"
              block
              style={{
                backgroundColor: "#8C7034",
                border: "none",
                height: 56,
                borderRadius: 9999,
                fontSize: "1.25rem",
                fontWeight: 300,
              }}
            >
              Забронировать
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}