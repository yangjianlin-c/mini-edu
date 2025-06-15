// 请求host更换, 后端地址
export const host = "http://127.0.0.1:8000";

// 课程等级映射
const levelMap: { [key: number]: string } = {
  1: "高级",
  2: "中级",
  3: "初级",
};

export function getLevel(key: number): string {
  return levelMap[key] || "未知";
}

// 图片完整url
export function getImageUrl(image: string): string {
  return `${host}${image}`;
}
