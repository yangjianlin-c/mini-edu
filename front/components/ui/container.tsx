import { cn } from "@/lib/utils"

interface ContainerProps extends React.HTMLAttributes<HTMLDivElement> {
  as?: React.ElementType
}

export function Container({
  className,
  as: Component = "div",
  ...props
}: ContainerProps) {
  return (
    <Component
      className={cn(
        "mx-auto w-full max-w-[1400px] px-4 md:px-6 lg:px-8",
        className
      )}
      {...props}
    />
  )
}