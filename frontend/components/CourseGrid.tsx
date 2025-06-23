import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
import { Tag } from "lucide-react"
import Image from 'next/image';
import Link from 'next/link';
import { Course } from "@/types/course";

interface CourseGridProps {
    courses: Course[];
}

const CourseGrid = ({ courses }: CourseGridProps) => {
    return (
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
            {courses.map((course) => (
                <Card key={course.id} className="pt-0">
                    <div className="overflow-hidden rounded-t-lg">
                        <Link href={`/course/${course.id}`}>
                            <Image
                                src={course.image ? course.image : `/${course.id}.png`}
                                alt={course.title}
                                width={400}
                                height={200}
                                className="h-auto w-auto object-cover transition-all hover:scale-105 aspect-[2/1]"
                            />
                        </Link>
                    </div>
                    <CardHeader>
                        <div className="text-sm text-muted-foreground pb-2 flex items-center gap-2">
                            <Tag className="h-4 w-4" />
                            ￥{course.price}
                        </div>
                        <Link href={`/course/${course.id}`}>
                            <CardTitle>{course.title}</CardTitle>
                        </Link>
                        <CardDescription>{course.description}</CardDescription>
                    </CardHeader>
                    <CardFooter>
                        <Button size="sm" asChild>
                            <Link href={`/course/${course.id}`}>查看详情</Link>
                        </Button>
                    </CardFooter>
                </Card>
            ))}
        </div>
    );
};

export default CourseGrid;
