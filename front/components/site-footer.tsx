import Link from "next/link"
import { Icons } from "@/components/icons"

export function SiteFooter() {
    return (
        <footer className="border-t py-12">
            <div className="mx-auto w-full max-w-[1400px] px-4 md:px-6 lg:px-8">
                <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
                    <div className="flex flex-col space-y-4">
                        <div className="flex items-center space-x-2">
                            <span className="font-bold">米克网</span>
                        </div>
                        <p className="text-sm text-muted-foreground">
                            米克网提供电电子产品散热解决方案，并分享热设计经验，旨在降低能耗，通过技术手段促进人与自然的和谐相处。
                        </p>
                        <div className="flex space-x-4">
                            <Link href="https://space.bilibili.com" className="text-muted-foreground hover:text-foreground" target="_blank" rel="noreferrer">
                                <Icons.bilibili className="h-5 w-5" />
                                <span className="sr-only">BiliBili</span>
                            </Link>
                            <Link href="https://github.com/mekesim" className="text-muted-foreground hover:text-foreground" target="_blank" rel="noreferrer">
                                <Icons.gitHub className="h-5 w-5" />
                                <span className="sr-only">GitHub</span>
                            </Link>
                        </div>
                        <div className="text-sm text-muted-foreground">
                            © 米克网 2023 - 2024. 浙ICP备100459259-6
                        </div>
                    </div>

                    {/* 第二列：Mekesim */}
                    <div className="flex flex-col space-y-4">
                        <h4 className="font-medium">Mekesim</h4>
                        <nav className="flex flex-col space-y-2">
                            <Link href="/courses" className="text-sm text-muted-foreground hover:text-foreground">
                                在线课程
                            </Link>
                            <Link href="/consulting" className="text-sm text-muted-foreground hover:text-foreground">
                                咨询服务
                            </Link>
                            <Link href="/contact" className="text-sm text-muted-foreground hover:text-foreground">
                                联系我们
                            </Link>
                        </nav>
                    </div>

                    <div className="flex flex-col space-y-4">
                        <h4 className="font-medium">关注我们</h4>             
                        <div className="flex space-x-8">
                            <div className="flex flex-col items-center">
                                <img src="/wechat-qrcode.png" alt="微信公众号二维码" className="w-20 h-20 rounded" />
                                <span className="text-xs text-muted-foreground mt-1">微信公众号</span>
                            </div>
                            <div className="flex flex-col items-center">
                                <img src="/bilibili-qrcode.png" alt="B站账号二维码" className="w-20 h-20 rounded" />
                                <span className="text-xs text-muted-foreground mt-1">B站账号</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    )
} 